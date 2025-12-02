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
    Simple rotor-like encryptor:
    - alphabet: printable ASCII characters (space .. ~)
    - _perm_from_seed(seed): create a shuffled permutation deterministically
      using random.Random(seed).
    - encrypt(plaintext): generate a random seed, build permutation, map chars,
      and return "seed:encoded".
    - decrypt(ciphertext): parse seed, rebuild permutation and reverse-map.
    """
    def __init__(self):
        # printable ASCII range (space .. ~)
        self.alphabet = [chr(i) for i in range(32, 127)]
        self.n = len(self.alphabet)

    def _perm_from_seed(self, seed: int):
        """
        Build a deterministic permutation of the alphabet using the provided seed.
        This uses a local Random so global PRNG state is not affected.
        """
        rng = random.Random(seed)
        perm = self.alphabet.copy()
        rng.shuffle(perm)
        return perm

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext by:
         - generating a random seed
         - building a permutation from the seed
         - mapping each character via the permutation
         - returning a string "<seed>:<encoded>" so decrypt can recover seed
        """
        seed = random.randint(0, 2**31 - 1)
        perm = self._perm_from_seed(seed)
        mapping = {self.alphabet[i]: perm[i] for i in range(self.n)}
        encoded = ''.join(mapping.get(ch, ch) for ch in plaintext)
        # store seed as header so decrypt can rebuild permutation
        return f"{seed}:{encoded}"

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext produced by encrypt():
         - split off the seed
         - rebuild the permutation
         - reverse-map characters to original
        Returns empty string on malformed input.
        """
        try:
            seed_str, encoded = ciphertext.split(":", 1)
            seed = int(seed_str)
        except Exception:
            return ""
        perm = self._perm_from_seed(seed)
        reverse = {perm[i]: self.alphabet[i] for i in range(self.n)}
        return ''.join(reverse.get(ch, ch) for ch in encoded)