import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import struct

from server.types.base import DataType

# Descargar recursos la primera vez
nltk.download('punkt')
nltk.download('stopwords')

# Recursos globales
_stop_words = set(stopwords.words('english'))
_stemmer = PorterStemmer()

def preprocess(text: str) -> list[str]:
    """
    Tokeniza, filtra stopwords, elimina signos y aplica stemming.
    """
    tokens = nltk.word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [t for t in tokens if t not in _stop_words]
    tokens = [_stemmer.stem(t) for t in tokens]
    return tokens

#print(preprocess("Hi everyone, my name is Rodri and I from Peru"))

class StringType(DataType[str]):
    def compare(self, other: 'StringType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "string",
            "value": self.value
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value.encode('utf-8'))
    
    def type_size(self) -> int:
        return len(self.value)
    
    def type_format(self) -> str:
        size = len(self.value)
        if size <= 0:
            raise ValueError("StringType requires a size parameter")
        return f'{size}s'
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'StringType':
        if data["type"] != "string":
            raise ValueError("Invalid type for StringType")
        return cls(data["value"])

    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        size = len(data)
        if size <= 0:
            raise ValueError("Invalid data size for StringType")
        format_str = f'{size}s'
        value = struct.unpack(format_str, data)[0].decode('utf-8').strip()
        return cls(value)

class TextType(DataType[str]):
    def compare(self, other: 'TextType') -> int:
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0
    
    def serialize(self) -> dict[str, any]:
        return {
            "type": "text",
            "value": self.value
        }
    
    def serialize_to_bytes(self) -> bytes:
        format_str = self.type_format()
        return struct.pack(format_str, self.value.encode('utf-8'))

    def type_size(self) -> int:
        return len(self.value)
    
    def type_format(self) -> str:
        size = len(self.value)
        if size <= 0:
            raise ValueError("TextType requires a size parameter")
        return f'{size}s'
    
    @classmethod
    def deserialize(cls, data: dict[str, any]) -> 'TextType':
        if data["type"] != "text":
            raise ValueError("Invalid type for TextType")
        return cls(data["value"]) 
    
    @classmethod
    def deserialize_from_bytes(cls, data: bytes) -> DataType:
        size = len(data)
        if size <= 0:
            raise ValueError("Invalid data size for TextType")
        format_str = f'{size}s'
        value = struct.unpack(format_str, data)[0].decode('utf-8').strip()
        return cls(value)