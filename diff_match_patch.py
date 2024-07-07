class DiffMatchPatch:
    """
    Implements the Diff Match Patch algorithm for computing differences between texts,
    finding matches within a text, and applying patches to transform one text into another.
    """

    def diff_main(self, text1, text2):
        """
        Compute the differences between two texts.
        Returns a list of tuples, where each tuple contains a diff operation (-1 for delete, 1 for insert, 0 for unchanged)
        and the corresponding substring.
        """
        if text1 == text2:
            return [(0, text1)]

        common_prefix_length = self._common_prefix(text1, text2)
        common_suffix_length = self._common_suffix(text1, text2)

        prefix = text1[:common_prefix_length]
        suffix = text1[len(text1) - common_suffix_length:]

        text1 = text1[common_prefix_length:len(text1) - common_suffix_length]
        text2 = text2[common_prefix_length:len(text2) - common_suffix_length]

        diffs = []
        if prefix:
            diffs.append((0, prefix))

        diffs.extend(self._diff_compute(text1, text2))

        if suffix:
            diffs.append((0, suffix))

        return diffs

    def _common_prefix(self, text1, text2):
        """
        Find the common prefix of two texts.
        Returns the length of the common prefix.
        """
        n = min(len(text1), len(text2))
        for i in range(n):
            if text1[i] != text2[i]:
                return i
        return n

    def _common_suffix(self, text1, text2):
        """
        Find the common suffix of two texts.
        Returns the length of the common suffix.
        """
        n = min(len(text1), len(text2))
        for i in range(1, n + 1):
            if text1[-i] != text2[-i]:
                return i - 1
        return n

    def _diff_compute(self, text1, text2):
        """
        Find the differences between two texts using a simple greedy algorithm.
        Returns a list of tuples representing the differences.
        """
        diffs = []
        len1, len2 = len(text1), len(text2)
        i, j = 0, 0

        while i < len1 and j < len2:
            if text1[i] == text2[j]:
                # Find matching substring
                start = i
                while i < len1 and j < len2 and text1[i] == text2[j]:
                    i += 1
                    j += 1
                diffs.append((0, text1[start:i]))
            else:
                # Find non-matching substrings
                start_i, start_j = i, j
                while i < len1 and j < len2 and text1[i] != text2[j]:
                    i += 1
                    j += 1
                if start_i != i:
                    diffs.append((-1, text1[start_i:i]))
                if start_j != j:
                    diffs.append((1, text2[start_j:j]))

        if i < len1:
            diffs.append((-1, text1[i:]))
        if j < len2:
            diffs.append((1, text2[j:]))

        return diffs

    def match_main(self, text, pattern):
        """
        Find the best match of a substring in a text using a simple heuristic.
        Returns the index of the best match or -1 if no match is found.
        """
        pattern_length = len(pattern)
        best_loc = -1
        best_score = float('inf')

        for i in range(len(text) - pattern_length + 1):
            score = sum(1 for j in range(pattern_length) if text[i + j] != pattern[j])
            if score < best_score:
                best_loc = i
                best_score = score

        return best_loc

    def patch_make(self, text1, text2):
        """
        Create a list of patches to convert text1 into text2.
        Returns a list of dictionaries, where each dictionary contains details about a patch.
        """
        diffs = self.diff_main(text1, text2)
        patches = []
        start = 0

        for diff in diffs:
            if diff[0] == 0:
                start += len(diff[1])
                continue
            patch = {
                'start': start,
                'delete': diff[1] if diff[0] == -1 else '',
                'insert': diff[1] if diff[0] == 1 else ''
            }
            if diff[0] == -1:
                start += len(diff[1])
            patches.append(patch)

        return patches

    def patch_apply(self, patches, text):
        """
        Apply a list of patches to a text.
        Returns the modified text after applying all patches.
        """
        shift = 0
        for patch in patches:
            start = patch['start'] + shift
            end = start + len(patch['delete'])
            text = text[:start] + patch['insert'] + text[end:]
            shift += len(patch['insert']) - len(patch['delete'])

        return text

