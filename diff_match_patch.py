# diff_match_patch.py

class DiffMatchPatch:
    def diff_main(self, text1, text2):
        """Compute the differences between two texts."""
        diffs = []
        i, j = 0, 0

        while i < len(text1) and j < len(text2):
            if text1[i] == text2[j]:
                i += 1
                j += 1
            else:
                start_i, start_j = i, j
                while i < len(text1) and j < len(text2) and text1[i] != text2[j]:
                    i += 1
                    j += 1
                diffs.append((start_i, start_j, i - start_i, j - start_j))
        
        if i < len(text1):
            diffs.append((i, j, len(text1) - i, 0))
        if j < len(text2):
            diffs.append((i, j, 0, len(text2) - j))

        return diffs

    def match_main(self, text, pattern):
        """Find the best match of a substring in a text."""
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
        """Create a list of patches to convert text1 into text2."""
        diffs = self.diff_main(text1, text2)
        patches = []
        
        for start1, start2, len1, len2 in diffs:
            patch = {
                'start1': start1,
                'start2': start2,
                'delete': text1[start1:start1+len1],
                'insert': text2[start2:start2+len2]
            }
            patches.append(patch)
        
        return patches

    def patch_apply(self, patches, text):
        """Apply a list of patches to a text."""
        shift = 0
        for patch in patches:
            start = patch['start1'] + shift
            end = start + len(patch['delete'])
            text = text[:start] + patch['insert'] + text[end:]
            shift += len(patch['insert']) - len(patch['delete'])
        
        return text


