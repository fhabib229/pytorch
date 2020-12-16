import torch
from torch.utils.data import IterableDataset
from torch.utils.data.datasets import (CollateIterableDataset)
from torch.testing._internal.common_utils import (TestCase, run_tests)


class IterDatasetWithoutLen(IterableDataset):
    def __init__(self, ds):
        super().__init__()
        self.ds = ds

    def __iter__(self):
        for i in self.ds:
            yield i


class IterDatasetWithLen(IterableDataset):
    def __init__(self, ds):
        super().__init__()
        self.ds = ds
        self.length = len(ds)

    def __iter__(self):
        for i in self.ds:
            yield i

    def __len__(self):
        return self.length


class TestFunctionalIterableDataset(TestCase):
    def test_collate_dataset(self):
        arrs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        ds_len = IterDatasetWithLen(arrs)
        ds_nolen = IterDatasetWithoutLen(arrs)

        def _collate_fn(batch):
            return torch.tensor(sum(batch), dtype=torch.float)

        collate_ds = CollateIterableDataset(ds_len, collate_fn=_collate_fn)
        self.assertEqual(len(ds_len), len(collate_ds))
        ds_iter = iter(ds_len)
        for x in collate_ds:
            y = next(ds_iter)
            self.assertEqual(x, torch.tensor(sum(y), dtype=torch.float))

        collate_ds_nolen = CollateIterableDataset(ds_nolen)
        with self.assertRaises(NotImplementedError):
            len(collate_ds_nolen)
        ds_nolen_iter = iter(ds_nolen)
        for x in collate_ds_nolen:
            y = next(ds_nolen_iter)
            self.assertEqual(x, torch.tensor(y))


if __name__ == '__main__':
    run_tests()
