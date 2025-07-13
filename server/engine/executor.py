import csv
import time
import os
from pathlib import Path
from dataclasses import dataclass, field
from sqlglot.expressions import Create, Insert, Delete, Drop, Select, Expression, Copy

from server.sql.sql_parser import SQLParser
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder

from server.catalog.catalog import CatalogService
from server.catalog.database import DatabaseService
from server.catalog.schema import SchemaService
from server.catalog.table import TableService
from server.catalog.column import ColumnService, Column
from server.catalog.index import IndexService

from server.storage.indexes.heap import HeapFile
from server.storage.indexes.Spimi import SpimiIndex

## music
from server.utils.audio import (
    obtener_recomendaciones_por_audio_mp3,
    obtener_recomendaciones_por_audio_wav,
    obtener_recomendaciones_por_song_id
)

@dataclass
class PinPom:
    base_path: Path = Path("data")
    file_manager: FileManager = field(default_factory=lambda: FileManager(Path("data")))
    path_builder: PathBuilder = field(default_factory=lambda: PathBuilder(Path("data")))
    sql_parser: SQLParser = field(default_factory=lambda: SQLParser())

    def __post_init__(self):
        self.catalog_service = CatalogService(self.file_manager, self.path_builder, self.base_path)
        self.database_service = DatabaseService(self.file_manager, self.path_builder, self.catalog_service)
        self.schema_service = SchemaService(self.file_manager, self.path_builder, self.database_service)
        self.table_service = TableService(self.file_manager, self.path_builder, self.schema_service)
        self.index_service = IndexService(self.file_manager, self.path_builder, self.table_service)
        self.database_global: str = "university" #"ppsql"
        self.schema_global: str = "course" #"public"

    def execute(self, sql: str) -> None:

        explain_mode = False
        sql_clean = sql.strip()

        if sql_clean.upper().startswith("EXPLAIN ANALYZE"):
            explain_mode = True
            sql_clean = sql_clean[len("EXPLAIN ANALYZE"):].strip()

        exprs = self.sql_parser.parse(sql_clean)
        results = []

        for expr in exprs:
            print(expr)  # <-- agrega esto
            print(repr(expr))  # <-- y esto
            try:
                operation = type(expr).__name__.upper().replace("EXPRESSION", "")
                table_name = "unknown"
                strategy = "Sequential Scan"
                condition = "-"
                algorithm = "-"

                if explain_mode:
                    start = time.perf_counter()

                if isinstance(expr, Copy):
                    result = self.copy_op(expr)
                elif isinstance(expr, Create):
                    result = self.create_op(expr)
                elif isinstance(expr, Drop):
                    result = self.drop_op(expr)
                elif isinstance(expr, Select):
                    parser = self.sql_parser._parse_select_from(expr)
                    table_name = parser.get('table', 'unknown')
                    condition_dict = parser.get('conditions')
                    limit = parser.get('limit')

                    if condition_dict:
                        if condition_dict['type'] == 'COSENO':
                            strategy = "Audio Similarity (coseno)"
                            algorithm = 'coseno'
                            condition = "path_download_wav <-> audio"
                        elif condition_dict['type'] == 'MANHATAN':
                            strategy = "Audio Similarity (manhattan)"
                            algorithm = 'manhattan'
                            condition = "path_download_wav <#> audio"
                        elif condition_dict['type'] == 'LINEAL':
                            strategy = "Audio Similarity (euclidiana)"
                            algorithm = 'euclidiana'
                            condition = "path_download_wav <=> audio"
                        elif condition_dict['type'] in ['EQ', 'LT']:
                            condition = f"{condition_dict['column']} {condition_dict['type']} {condition_dict['value']}"
                            strategy = "Index Scan" if IndexService.call_index_by_name(
                                self.table_service.get_table(self.database_global, self.schema_global,
                                                             table_name).tab_indexes,
                                condition_dict['column']
                            ) else "Sequential Scan"
                    result = self.select_op(expr)
                    return result
                elif isinstance(expr, Insert):
                    result = self.insert_op(expr)
                elif isinstance(expr, Delete):
                    result = self.delete_op(expr)
                else:
                    raise ValueError(f"Operation not supported: {type(expr)}")

                if explain_mode:
                    end = time.perf_counter()
                    duration_ms = round((end - start), 3)
                    explain_result = [
                        "[INFO] Execution Plan:",
                        f"  • Operation: {operation}",
                        f"  • Table: {table_name}",
                        f"  • Condition: {condition}",
                        f"  • Strategy: {strategy}",
                        f"  • Algorithm: {algorithm}",
                        f"  • Execution Time: {duration_ms} ms"
                    ]
                    results.append("\n".join(explain_result))
                elif result is not None:
                    results.append(result)

            except Exception as e:
                print(f"Error in building: {str(e)}")
                continue

        return results

    def drop_op(self, expr: Expression):
        if expr.kind == "TABLE":
            parser = self.sql_parser._parse_drop_table(expr)
        elif expr.kind == "DATABASE":
            parser = self.sql_parser._parse_drop_database(expr)
        elif expr.kind == "SCHEMA":
            parser = self.sql_parser._parse_drop_schema(expr)
    def create_op(self, expr: Expression):
        if expr.kind == "TABLE":
            parser = self.sql_parser._parse_create_table(expr)
            self.table_service.create_table(
                db_name=self.database_global,
                sch_name=self.schema_global,
                tab_name=parser['name'],
                columns=parser['columns']
            )

            self.index_service.create_index(
                db_name=self.database_global,
                sch_name=self.schema_global,
                tab_name=parser['name'],
                idx_name="primary_key",
                idx_type="btree",
                idx_column="id", # assuming 'id' is the primary key column
                idx_is_primary=True
            )
            return
        if expr.kind == "DATABASE":
            parser = self.sql_parser._parse_create_database(expr)
            db_name = parser['name']
            self.database_service.create_database(db_name)
            self.database_global = db_name
            return
        if expr.kind == "SCHEMA":
            parser = self.sql_parser._parse_create_schema(expr)
            sch_name = parser['name']
            self.schema_service.create_schema(
                db_name=self.database_global,
                sch_name=sch_name
            )
            self.schema_global = sch_name
            return
        if expr.kind == "INDEX":
            parser = self.sql_parser._parse_create_index(expr)
            if parser['type'] == "spimi":
                # Construcción del índice SPIMI desde la tabla y columna indicada
                table = self.table_service.get_table(
                    self.database_global,
                    self.schema_global,
                    parser['table']
                )
                column_name = parser['column']
                heap_file = self.path_builder.table_data(self.database_global, self.schema_global, parser['table'])
                heap = HeapFile(heap_file, table.tab_columns)
                all_records = heap.get_all_records()
                lyrics_index = next(i for i, col in enumerate(table.tab_columns) if col.att_name == column_name)
                lyrics_list = [record[lyrics_index].value for record in all_records]

                path_save = f"C:/Users/USUARIO/PycharmProjects/supabase-reply/server/storage/indexes/spimi_indexes/{parser['table']}_{column_name}"
                spimi = SpimiIndex(lyrics_list, path_save, inicializar_hp=True)

                print(f"[INFO] SPIMI index creado y guardado en {path_save}")
                return
            self.index_service.create_index(
                db_name=self.database_global,
                sch_name=self.schema_global,
                tab_name=parser['table'],
                idx_name=parser['name'],
                idx_type=parser['type'],
                idx_column=parser['column'],
                idx_is_primary=False
            )
            return
    def select_op(self, expr: Expression):
        parser = self.sql_parser._parse_select_from(expr)
        params = parser['params']
        conditions = parser['conditions']
        limit = parser.get('limit')
        distintc = parser.get('distinct')
        table = self.table_service.get_table(self.database_global, self.schema_global, parser['table'])
        heap_file = self.path_builder.table_data(self.database_global, self.schema_global, table.tab_name)
        heap = HeapFile(heap_file, table.tab_columns)
        if conditions:
            # Caso SPIMI: buscar vecinos más cercanos con WHERE columna @@ 'texto'
            if isinstance(conditions, dict) and conditions.get("type") in {"SPIMI_MATCH", "AND", "OR", "AND_NOT"}:

                def extract_spimi_queries(cond):
                    """
                    Retorna la columna usada y las cadenas de texto de cada SPIMI_MATCH involucrado.
                    También verifica que todas usen la misma columna.

                    Soporta:
                    - SPIMI_MATCH
                    - AND
                    - OR
                    - AND NOT (como combinación AND con NOT a la derecha)
                    """
                    if cond["type"] == "SPIMI_MATCH":
                        return cond["column"], [cond["value"]], "SPIMI_MATCH"

                    elif cond["type"] == "AND":
                        # Detectamos si el segundo operando es un NOT
                        right = cond["right"]

                        if isinstance(right, dict) and right.get("type") == "NOT":
                            # Esto es un AND_NOT
                            col_left, val_left, _ = extract_spimi_queries(cond["left"])
                            col_right, val_right, _ = extract_spimi_queries(right["operand"])
                            if col_left != col_right:
                                raise ValueError("Todas las condiciones @@ deben usar la misma columna")
                            return col_left, [val_left[0], val_right[0]], "AND_NOT"
                        else:
                            # AND normal
                            col_left, val_left, _ = extract_spimi_queries(cond["left"])
                            col_right, val_right, _ = extract_spimi_queries(cond["right"])
                            if col_left != col_right:
                                raise ValueError("Todas las condiciones @@ deben usar la misma columna")
                            return col_left, [val_left[0], val_right[0]], "AND"

                    elif cond["type"] == "OR":
                        col_left, val_left, _ = extract_spimi_queries(cond["left"])
                        col_right, val_right, _ = extract_spimi_queries(cond["right"])
                        if col_left != col_right:
                            raise ValueError("Todas las condiciones @@ deben usar la misma columna")
                        return col_left, [val_left[0], val_right[0]], "OR"

                    else:
                        raise ValueError(f"Operación SPIMI no soportada: {cond['type']}")

                column, query_list, spimi_op = extract_spimi_queries(conditions)

                path_spimi = f"C:/Users/USUARIO/PycharmProjects/supabase-reply/server/storage/indexes/spimi_indexes/{table.tab_name}_{column}"
                if not os.path.exists(path_spimi):
                    raise FileNotFoundError(f"[ERROR] SPIMI index file not found in {path_spimi}")

                spimi = SpimiIndex([], path_spimi, inicializar_hp=False)
                k = limit if limit else 5
                if spimi_op == "SPIMI_MATCH":
                    vecinos = spimi.query_knn(query_list[0], k=k)
                elif spimi_op == "AND":
                    vecinos = spimi.AND(query_list[0], query_list[1])
                elif spimi_op == "OR":
                    vecinos = spimi.OR(query_list[0], query_list[1])
                elif spimi_op == "AND_NOT":
                    vecinos = spimi.AND_NOT(query_list[0], query_list[1])
                else:
                    raise ValueError("Operador SPIMI no implementado")

                print(vecinos)
                print("")

                # Filtrar por ID
                column_primary = table.tab_columns[0]
                ids = []
                for v in vecinos:
                    if isinstance(v, (list, tuple)):
                        doc_id = v[0]  # (id, score)
                    else:
                        doc_id = v  # sólo id
                    ids.append(
                        ColumnService.to_type(column_primary.att_type_id, doc_id, type_size=column_primary.att_len)
                    )

                condition_in = {
                    'type': 'IN',
                    'column': 'id',
                    'value': ids
                }

                result = heap.get_all_records_json(params, limit, distintc, condition_in)
                return result
            new_conditions = self.tranform_type_conditions(conditions, table.tab_columns)
            index = IndexService.call_index_by_name(table.tab_indexes, new_conditions['column'])
            if index:
                if new_conditions['type'] == 'EQ':
                    index.search(new_conditions['value'])
                    result = heap.get_record_json(params, new_conditions)
                    return result
                elif new_conditions['type'] == 'LT': # change
                    index.search(new_conditions['value'])
                    result = heap.get_record_json(params, new_conditions)
                    return result
            else:
                if conditions['type'] == 'COSENO':
                    filepath = conditions['value']
                    k = limit if limit else 5
                    recommendations = obtener_recomendaciones_por_audio_wav(filepath, k, "coseno")
                    column_primary = table.tab_columns[0]
                    condition_in = {
                        'type': 'IN',
                        'column': 'id',
                        'value': [
                            ColumnService.to_type(column_primary.att_type_id, value, type_size=column_primary.att_len)
                            for value in recommendations.keys()
                        ]
                    }
                    result = heap.get_all_records_json(params, limit, distintc, condition_in)
                    return result
                elif conditions['type'] == 'MANHATAN':
                    filepath = conditions['value']
                    k = limit if limit else 5
                    recommendations = obtener_recomendaciones_por_audio_wav(filepath, k, "manhatan")
                    column_primary = table.tab_columns[0]
                    condition_in = {
                        'type': 'IN',
                        'column': 'id',
                        'value': [
                            ColumnService.to_type(column_primary.att_type_id, value, type_size=column_primary.att_len)
                            for value in recommendations.keys()
                        ]
                    }
                    result = heap.get_all_records_json(params, limit, distintc, condition_in)
                    return result
                elif conditions['type'] == 'LINEAL':
                    filepath = conditions['value']
                    k = limit if limit else 5
                    recommendations = obtener_recomendaciones_por_audio_wav(filepath, k, "euclidiana") # REF TO LINEAL
                    column_primary = table.tab_columns[0]
                    condition_in = {
                        'type': 'IN',
                        'column': 'id',
                        'value': [
                            ColumnService.to_type(column_primary.att_type_id, value, type_size=column_primary.att_len)
                            for value in recommendations.keys()
                        ]
                    }
                    result = heap.get_all_records_json(params, limit, distintc, condition_in)
                    return result
            result = heap.get_all_records_json(params, limit, distintc, new_conditions)
            return result
        result = heap.get_all_records_json(params, limit, distintc, None)
        return result
    
    def copy_op(self, expr: Expression):
        parser = self.sql_parser._parse_copy_from(expr)
        table = self.table_service.get_table(self.database_global, self.schema_global, parser['table'])
        heap_file = self.path_builder.table_data(self.database_global, self.schema_global, table.tab_name)
        heap = HeapFile(heap_file, table.tab_columns)
        indexes = IndexService.call_indexes(table.tab_indexes, table.tab_columns)
        with open(parser['file'], 'r', encoding='utf-8') as f:
            lector = csv.reader(f)
            next(lector)
            for row in lector:
                data = []
                for col, value in zip(table.tab_columns, row):
                    data_type = ColumnService.to_type(col.att_type_id, value, type_size=col.att_len)
                    data.append(data_type)
                position = heap.insert(data)
                for call in indexes:
                    data_type_instance = data[call['column_index']]
                    call['index'].insert(data_type_instance, position)
            
    def delete_op(self, expr: Expression):
        parser = self.sql_parser._parse_delete_from_table(expr)
    def insert_op(self, expr: Expression):
        parser = self.sql_parser._parse_insert_into_values(expr)
        table = self.table_service.get_table(self.database_global, self.schema_global, parser['table'])
        heap_file = self.path_builder.table_data(self.database_global, self.schema_global, table.tab_name)
        heap = HeapFile(heap_file, table.tab_columns)
        indexes = IndexService.call_indexes(table.tab_indexes, table.tab_columns)
        for row in parser['values']:
            data = []
            for col, value in zip(table.tab_columns, row):
                data_type = ColumnService.to_type(col.att_type_id, value, type_size=col.att_len)
                data.append(data_type)
            position = heap.insert(data)
            for call in indexes:
                data_type_instance = data[call['column_index']]
                call['index'].insert(data_type_instance, position)
    def set_database(self, db_name) -> None:
        self.database = db_name
    def set_schema(self, schema_name) -> None:
        self.schema = schema_name

    def get_top_music(self, id: int):
        songs = obtener_recomendaciones_por_song_id(id, tipo='manhatan',k=5)
        key_list = ', '.join(str(k) for k in songs)
        query = f"""
            SELECT id, track_name, track_artist, image_url
            FROM music
            WHERE id IN ({key_list})
        """
        return self.execute(query)

    @classmethod
    def tranform_type_conditions(cls, condition: dict, columns: list[Column]) -> dict:
        if condition['type'] == 'AND':
            return {
                'type': 'AND',
                'left': cls.tranform_type_conditions(condition['left'], columns),
                'right': cls.tranform_type_conditions(condition['right'], columns)
            }
        elif condition['type'] == 'OR':
            return {
                'type': 'OR',
                'left': cls.tranform_type_conditions(condition['left'], columns),
                'right': cls.tranform_type_conditions(condition['right'], columns)
            }
        else:
            column_name = condition['column']
            column = next((col for col in columns if col.att_name == column_name), None)
            if not column:
                raise ValueError(f"Column {column_name} not found in table.")
            if condition['type'] == "BETWEEN":
                return {
                    'type': 'BETWEEN',
                    'column': column.att_name,
                    'low': ColumnService.to_type(column.att_type_id, condition['low'], type_size=column.att_len),
                    'high': ColumnService.to_type(column.att_type_id, condition['high'], type_size=column.att_len)
                }
            elif condition['type'] == "IN":
                return {
                    'type': condition['type'],
                    'column': column_name,
                    'value': [
                        ColumnService.to_type(column.att_type_id, value, type_size=column.att_len)
                        for value in condition['value']
                    ]
                }
            else:
                return {
                    'type': condition['type'],
                    'column': column_name,
                    'value': ColumnService.to_type(column.att_type_id, condition['value'], type_size=column.att_len)
                }