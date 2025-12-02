"""
author : Leo L. and Jeff J.
date   : oct 30
desc   : Simple rotor-like encryptor that generates a deterministic permutation
         from a random seed. The seed is prepended to the ciphertext as
         "seed:..." so decrypt can reconstruct the mapping without external files.
         The module provides Encrypt.encrypt(plaintext) -> ciphertext and
         Encrypt.decrypt(ciphertext) -> plaintext.
"""
import random

class Encrypt:
    """
    Simple rotor-like encryptor using a random seed header "seed:payload".
    encrypt(plaintext) -> "seed:encoded"
    decrypt(ciphertext) -> plaintext or "" on failure
    """
    def __init__(self):
        # printable ASCII from space (32) to tilde (126)
        self.alphabet = [chr(i) for i in range(32, 127)]
        self.n = len(self.alphabet)

    def _perm_from_seed(self, seed: int):
        rng = random.Random(seed)
        perm = self.alphabet.copy()
        rng.shuffle(perm)
        return perm

    def encrypt(self, plaintext: str) -> str:
        seed = random.randint(0, 2**31 - 1)
        perm = self._perm_from_seed(seed)
        mapping = {self.alphabet[i]: perm[i] for i in range(self.n)}
        encoded = ''.join(mapping.get(ch, ch) for ch in plaintext)
        return f"{seed}:{encoded}"

    def decrypt(self, ciphertext: str) -> str:
        # expect "seed:payload"
        try:
            seed_str, encoded = ciphertext.split(":", 1)
            seed = int(seed_str)
        except Exception:
            return ""
        try:
            perm = self._perm_from_seed(seed)
            reverse = {perm[i]: self.alphabet[i] for i in range(self.n)}
            return ''.join(reverse.get(ch, ch) for ch in encoded)
        except Exception:
            return ""

    # fallback for files produced with the old custom alphabet
    def decrypt_old(self, ciphertext: str) -> str:
        """
        Attempt decrypt using the legacy alphabet (A..Z + symbols).
        Returns plaintext or empty string on failure.
        """
        try:
            seed_str, encoded = ciphertext.split(":", 1)
            seed = int(seed_str)
        except Exception:
            return ""
        OLD_ALPHABET = [chr(i) for i in range(65, 91)] + [",", ".", "!", "/", "?", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+"]
        try:
            rng = random.Random(seed)
            perm = OLD_ALPHABET.copy()
            rng.shuffle(perm)
            rev = {perm[i]: OLD_ALPHABET[i] for i in range(len(OLD_ALPHABET))}
            return ''.join(rev.get(ch, ch) for ch in encoded)
        except Exception:
            return ""