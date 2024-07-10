class DiffMatchPatch:

    def diff_main(self, text1, text2):
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
        n = min(len(text1), len(text2))
        for i in range(n):
            if text1[i] != text2[i]:
                return i
        return n

    def _common_suffix(self, text1, text2):
        n = min(len(text1), len(text2))
        for i in range(1, n + 1):
            if text1[-i] != text2[-i]:
                return i - 1
        return n

    def _diff_compute(self, text1, text2):
        if not text1:
            return [(1, text2)]
        if not text2:
            return [(-1, text1)]

        len1, len2 = len(text1), len(text2)
        diffs = []

        i, j = 0, 0
        while i < len1 and j < len2:
            if text1[i] == text2[j]:
                start = i
                while i < len1 and j < len2 and text1[i] == text2[j]:
                    i += 1
                    j += 1
                diffs.append((0, text1[start:i]))
            else:
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

        merged_diffs = self._merge_diffs(diffs)
        return merged_diffs

    def _merge_diffs(self, diffs):
        if not diffs:
            return []

        merged_diffs = [diffs[0]]
        for diff in diffs[1:]:
            if diff[0] == merged_diffs[-1][0]:
                merged_diffs[-1] = (merged_diffs[-1][0], merged_diffs[-1][1] + diff[1])
            else:
                merged_diffs.append(diff)

        return merged_diffs

    def match_main(self, text, pattern):
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
        shift = 0
        for patch in patches:
            start = patch['start'] + shift
            end = start + len(patch['delete'])
            text = text[:start] + patch['insert'] + text[end:]
            shift += len(patch['insert']) - len(patch['delete'])

        return text