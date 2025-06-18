from sqlglot import parse as parse_glot
from sqlglot.dialects.postgres import Postgres
from sqlglot.expressions import *
from dataclasses import dataclass

from server.catalog.column import Column as ColumnModel
from server.enums.data_type_enum import (
    DataTypeLabel, 
    IntegerTypeSize, 
    TemporalTypeSize,
    OtherTypeSize,
)

@dataclass
class SQLParser:
    
    def parse(self, sql: str) -> dict[str, any]:
        return parse_glot(sql, dialect=Postgres)
        
    def _parse_create_table(self, expr: Expression) -> dict[str, any]:
        table_dict = {}
        table_name = expr.find(Table).this.name
        columns = []
        for column in expr.find_all(ColumnDef):
            column_name = column.find(Identifier).this
            data_type = column.find(DataType)
            column_type = DataTypeLabel[data_type.this.name].value
            column_len = None
            if data_type.this in DataType.TEXT_TYPES:
                column_len = data_type.find(Literal).to_py()
            elif column_name.lower() == "uuid":
                column_len = OtherTypeSize[column_name.upper()].value
            elif data_type.this in DataType.INTEGER_TYPES:
                column_len = IntegerTypeSize[data_type.this.name].value
            elif data_type.this in DataType.TEMPORAL_TYPES:
                column_len = TemporalTypeSize[data_type.this.name].value
            
            column_not_null = False
            if column.find(PrimaryKeyColumnConstraint) or column.find(NotNullColumnConstraint):
                column_not_null = True
            column_has_def = False
            column_model = ColumnModel(
                column_name,
                column_type,
                column_len,
                column_not_null,
                column_has_def
            )
            columns.append(column_model)
        
        table_dict['name'] = table_name
        table_dict['columns'] = columns
        return table_dict
    
    def _parse_create_index(self, expr: Expression) -> dict[str, any]:
        index_dict = {}
        index_dict['name'] = expr.find(Identifier).this
        index_dict['table'] = expr.find(Table).this.name
        params = expr.find(IndexParameters)
        index_dict['type'] = params.args.get('using').this.lower()
        index_dict['column'] = params.find(Identifier).this
        return index_dict
    
    def _parse_create_database(self, expr: Expression) -> dict[str, any]:
        db_dict = {}
        db_dict['name'] = expr.find(Identifier).this
        return db_dict
    
    def _parse_create_schema(self, expr: Expression) -> dict[str, any]:
        sch_dict = {}
        sch_dict['name'] = expr.find(Identifier).this
        return sch_dict

    def _parse_drop_table(self, expr: Expression) -> dict[str, any]:
        tab_dict = {}
        tab_dict['name'] = expr.find(Identifier).this
        return tab_dict
    
    def _parse_drop_schema(self, expr: Expression) -> dict[str, any]:
        sch_dict = {}
        sch_dict['name'] = expr.find(Identifier).this
        return sch_dict
    
    def _parse_drop_database(self, expr: Expression) -> dict[str, any]:
        db_dict = {}
        db_dict['name'] = expr.find(Identifier).this
        return db_dict
    
    def _parse_insert_into_values(self, expr: Expression) -> dict[str, any]:
        # is sort attr (a,b,c,d ...)
        insert_dict = {}
        insert_dict['table'] = expr.find(Table).this.name
        values = []
        for v in expr.find_all(Tuple):
            rows = []
            for row in v.find_all(Literal):
                rows.append(row.to_py())
            values.append(tuple(rows))
        insert_dict['values'] = values
        return insert_dict
    
    def _parse_select_from(self, expr: Expression) -> dict[str, any]:
        
        select_dict = {}
        select_dict['table'] = expr.args.get('from').find(Table).find(Identifier).this
        params = []
        for exp in expr.args.get('expressions'):
            if isinstance(exp, Star):
                params.append("*")
            else:
                params.append(exp.find(Identifier).this)
        select_dict['params'] = params
        conditions = []
        where_exp = expr.args.get('where')
        if where_exp is not None:
            conditions = self.parse_condition(where_exp.this)

        select_dict['conditions'] = conditions
        return select_dict
    
    def _parse_delete_from_table(self, expr: Expression) -> dict[str, any]:
        delete_dict = {}
        delete_dict['table'] = expr.find(Table).find(Identifier).this
        conditions = []
        where_exp = expr.args.get('where')
        if where_exp is not None:
            conditions = self.parse_condition(where_exp.this)

        delete_dict['conditions'] = conditions
        return delete_dict
    
    @classmethod
    def parse_condition(cls, where_exp):
        if isinstance(where_exp, Between):
            condition = {
                'type': "BETWEEN",
                'column': where_exp.find(Identifier).this,
                'low': where_exp.args.get('low').find(Literal).to_py(),
                'high': where_exp.args.get('high').find(Literal).to_py()
            }
            return condition
        elif isinstance(where_exp, (And, Or)):
            left = where_exp.args.get('this')
            right = where_exp.args.get('expression')
            return {
                'type': "AND" if isinstance(where_exp, And) else "OR",
                'left': cls.parse_condition(left),
                'right': cls.parse_condition(right)
            }
        elif isinstance(where_exp, (LT, LTE, GT, GTE, EQ, NEQ)):
            condition = {
                'type': {
                    LT: "LT",
                    LTE: "LTE",
                    GT: "GT",
                    GTE: "GTE",
                    EQ: "EQ",
                    NEQ: "NEQ"
                }[type(where_exp)],
                'column': where_exp.find(Identifier).this,
                'value': where_exp.find(Literal).to_py()
            }
            return condition
        elif isinstance(where_exp, MatchAgainst):
            return {
                'type': "MATCHAGAINST",
                'column': where_exp.find(Identifier).this,
                'value': where_exp.find(Literal).this
            }
        return None

    