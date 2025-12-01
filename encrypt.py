import random

class Encrypt:
    """
    Simple rotor-like encryptor that generates a deterministic permutation
    from a random seed. The seed is prepended to the ciphertext as "seed:..."
    so decrypt can reconstruct the mapping without external files.
    """
    def __init__(self):
        # printable ASCII range (space .. ~)
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
        # store seed as header so decrypt can rebuild permutation
        return f"{seed}:{encoded}"

    def decrypt(self, ciphertext: str) -> str:
        try:
            seed_str, encoded = ciphertext.split(":", 1)
            seed = int(seed_str)
        except Exception:
            return ""
        perm = self._perm_from_seed(seed)
        reverse = {perm[i]: self.alphabet[i] for i in range(self.n)}
        return ''.join(reverse.get(ch, ch) for ch in encoded)