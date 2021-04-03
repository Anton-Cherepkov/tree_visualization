from collections.abc import Iterable


class TreeContours:
    def __init__(self, left_contour=list(), right_contour=list(),
                    left_contour_offsets_from_root=list(),
                    right_contour_offsets_from_root=list()):
        assert isinstance(left_contour, Iterable) 
        assert isinstance(right_contour, Iterable)
        assert isinstance(left_contour_offsets_from_root, Iterable)
        assert isinstance(right_contour_offsets_from_root, Iterable)

        self.left_contour  = left_contour
        self.right_contour = right_contour

        self.left_contour_offsets_from_root  = left_contour_offsets_from_root
        self.right_contour_offsets_from_root = right_contour_offsets_from_root

        assert len(left_contour)  == len(left_contour_offsets_from_root)
        assert len(right_contour) == len(right_contour_offsets_from_root)
    
    def __len__(self):
        return max(len(self.left_contour), len(self.right_contour))
    
    def add_offset(self, offset):
        for i in range(len(self.left_contour_offsets_from_root)):
            self.left_contour_offsets_from_root[i] += offset
        for i in range(len(self.right_contour_offsets_from_root)):
            self.right_contour_offsets_from_root[i] += offset
    
    def extend(self, node, offset):
        self.left_contour  = [node,] + self.left_contour
        self.right_contour = [node,] + self.right_contour

        self.left_contour_offsets_from_root  = [offset,] + self.left_contour_offsets_from_root
        self.right_contour_offsets_from_root = [offset,] + self.right_contour_offsets_from_root
    
    @staticmethod
    def merge_contours(left, right, node, left_offset, right_offset):
        height_left = len(left)
        height_right = len(right)

        left.add_offset(left_offset)
        right.add_offset(right_offset)

        left_contour  = [node,] + left.left_contour + right.left_contour[height_left:]
        right_contour = [node,] + right.right_contour + left.right_contour[height_right:]

        left_contour_offsets_from_root   = [0,]
        left_contour_offsets_from_root  += left.left_contour_offsets_from_root
        left_contour_offsets_from_root  += right.left_contour_offsets_from_root[height_left:]

        right_contour_offsets_from_root  = [0,]
        right_contour_offsets_from_root += right.right_contour_offsets_from_root
        right_contour_offsets_from_root += left.right_contour_offsets_from_root[height_right:]

        return TreeContours(left_contour, right_contour, left_contour_offsets_from_root, right_contour_offsets_from_root)
