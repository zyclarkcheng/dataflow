import tensorpack.dataflow as df

if __name__ == '__main__':
    ds = df.dataset.Cifar10('train')
    augmentors = [
        df.imgaug.RandomApplyAug(df.imgaug.RandomResize((0.8, 1.2), (0.8, 1.2)), 0.3),
        df.imgaug.RandomApplyAug(df.imgaug.RotationAndCropValid(15), 0.5),
        df.imgaug.RandomApplyAug(df.imgaug.SaltPepperNoise(white_prob=0.01, black_prob=0.01), 0.25),

        df.imgaug.Resize((32, 32)),
        df.imgaug.CenterPaste((36, 36)),
        df.imgaug.RandomCrop((32, 32)),

        df.imgaug.MapImage(lambda x: x.reshape(32, 32, 3))
    ]
    ds = df.AugmentImageComponent(ds, augmentors)
    ds = df.BatchData(ds, batch_size=32, remainder=False)
    ds = df.PrefetchData(ds, nr_prefetch=12, nr_proc=4)
    ds = df.PrintData(ds)

    df.TestDataSpeed(ds, size=50000/32).start()
