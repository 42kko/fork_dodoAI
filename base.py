import importlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Chunk:
    """Dataclass representing a text chunk with metadata."""

    text: str
    start_index: int
    end_index: int
    token_count: int


class BaseChunker(ABC):
    """Abstract base class for all chunker implementations.

    All chunker implementations should inherit from this class and implement
    the chunk() method according to their specific chunking strategy.
    """

    def __init__(self, tokenizer):
        """Initialize the chunker with a tokenizer.

        Args:
            tokenizer: Tokenizer object to be used for tokenizing text
        """
        if isinstance(tokenizer, str):
            self.tokenizer = self._load_tokenizer(tokenizer)
        else:
            self.tokenizer = tokenizer
            self._tokenizer_backend = self._get_tokenizer_backend()

    def _get_tokenizer_backend(self):
        """Return the backend tokenizer object."""
        if "transformers" in str(type(self.tokenizer)):
            return "transformers"
        elif "tokenizers" in str(type(self.tokenizer)):
            return "tokenizers"
        elif "tiktoken" in str(type(self.tokenizer)):
            return "tiktoken"
        else:
            raise ValueError("Tokenizer backend not supported")

    def _load_tokenizer(self, tokenizer_name: str):
        """Load a tokenizer based on the backend."""
        try:
            if importlib.util.find_spec("tiktoken") is not None:
                from tiktoken import get_encoding

                self._tokenizer_backend = "tiktoken"
                return get_encoding(tokenizer_name)
            else:
                raise Warning("TikToken library not found. Trying autotiktokenizer.")
        except Exception:
            try:
                if importlib.util.find_spec("autotiktokenizer") is not None:
                    from autotiktokenizer import AutoTikTokenizer

                    self._tokenizer_backend = "tiktoken"
                    return AutoTikTokenizer.from_pretrained(tokenizer_name)
                else:
                    raise Warning(
                        "AutoTikTokenizer library not found. Trying tokenizers."
                    )
            except Exception:
                try:
                    if importlib.util.find_spec("tokenizers") is not None:
                        from tokenizers import Tokenizer

                        self._tokenizer_backend = "tokenizers"
                        return Tokenizer.from_pretrained(tokenizer_name)
                    else:
                        raise Warning(
                            "Tokenizers library not found. Trying transformers."
                        )
                except Exception:
                    try:
                        if importlib.util.find_spec("transformers") is not None:
                            from transformers import AutoTokenizer

                            self._tokenizer_backend = "transformers"
                            return AutoTokenizer.from_pretrained(tokenizer_name)
                    except Exception:
                        raise ValueError(
                            "Tokenizer not found in the following libraries: transformers, tokenizers, autotiktokenizer, tiktoken",
                            "Please install one of these libraries to use the chunker.",
                        )

    def _encode(self, text: str):
        """Encode text using the backend tokenizer."""
        if self._tokenizer_backend == "transformers":
            return self.tokenizer.encode(text)
        elif self._tokenizer_backend == "tokenizers":
            return self.tokenizer.encode(text).ids
        elif self._tokenizer_backend == "tiktoken":
            return self.tokenizer.encode(text)
        else:
            raise ValueError("Tokenizer backend not supported.")

    def _encode_batch(self, texts: List[str]):
        """Encode a batch of texts using the backend tokenizer."""
        if self._tokenizer_backend == "transformers":
            return self.tokenizer.batch_encode_plus(texts)["input_ids"]
        elif self._tokenizer_backend == "tokenizers":
            return self.tokenizer.encode_batch(texts)
        elif self._tokenizer_backend == "tiktoken":
            return self.tokenizer.encode_batch(texts)
        else:
            raise ValueError("Tokenizer backend not supported.")

    def _decode(self, tokens) -> str:
        """Decode tokens using the backend tokenizer."""
        if self._tokenizer_backend == "transformers":
            return self.tokenizer.decode(tokens)
        elif self._tokenizer_backend == "tokenizers":
            return self.tokenizer.decode(tokens)
        elif self._tokenizer_backend == "tiktoken":
            return self.tokenizer.decode(tokens)
        else:
            raise ValueError("Tokenizer backend not supported.")

    def _decode_batch(self, token_lists: List[List[int]]) -> List[str]:
        """Decode a batch of token lists using the backend tokenizer."""
        if self._tokenizer_backend == "transformers":
            return [self.tokenizer.decode(tokens) for tokens in token_lists]
        elif self._tokenizer_backend == "tokenizers":
            return [self.tokenizer.decode(tokens) for tokens in token_lists]
        elif self._tokenizer_backend == "tiktoken":
            return [self.tokenizer.decode(tokens) for tokens in token_lists]
        else:
            raise ValueError("Tokenizer backend not supported.")

    @abstractmethod
    def chunk(self, text: str) -> List[Chunk]:
        """Split text into chunks according to the implementation strategy.

        Args:
            text: Input text to be chunked

        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        pass

    def __call__(self, text: str) -> List[Chunk]:
        """Make the chunker callable directly.

        Args:
            text: Input text to be chunked

        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        return self.chunk(text)

    def __repr__(self) -> str:
        """Return string representation of the chunker."""
        return f"{self.__class__.__name__}()"