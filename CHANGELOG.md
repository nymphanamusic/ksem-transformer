# Changelog

## 0.1.0 (2024-08-08)


### ⚠ BREAKING CHANGES

* Renamed MIDI controls to more closely match the names in KSEM configs.

### Features

* :sparkles: add automation settings ([3e537b1](https://github.com/nymphanamusic/ksem-transformer/commit/3e537b102ca9239f5d156e5b31eca40bf91a7925))
* :sparkles: add control_pad settings ([862b845](https://github.com/nymphanamusic/ksem-transformer/commit/862b8454109114e11e95cb8c8761f08b6077439a))
* :sparkles: add delay settings ([649514b](https://github.com/nymphanamusic/ksem-transformer/commit/649514b452bd1dfe4ff4868101ee19a1019b1168))
* :sparkles: add naive Notes ([784da7d](https://github.com/nymphanamusic/ksem-transformer/commit/784da7dbb97e091903ee11d33e239ea77ddc4f2d))
* :sparkles: add pitch_range and automation_key ([2dfdab6](https://github.com/nymphanamusic/ksem-transformer/commit/2dfdab6a672670ba53e8b84037d3d6a3355a5de4))
* :sparkles: add router and MPE settings ([bac8f58](https://github.com/nymphanamusic/ksem-transformer/commit/bac8f58bb737e8e265a9d362ac888ca6dfbbedfd))
* :sparkles: add send_main_key setting ([f56a2be](https://github.com/nymphanamusic/ksem-transformer/commit/f56a2be481831da58f8958e93940f170fcce36f0))
* :sparkles: add XY pad settings ([02e425d](https://github.com/nymphanamusic/ksem-transformer/commit/02e425dc87b149a3ecac4f95b539edcb32bb8c2c))
* :sparkles: generate keyswitch settings ([32f34d0](https://github.com/nymphanamusic/ksem-transformer/commit/32f34d0c2c314618ac2df938330eff9f5b06b62e))
* :tada: initial commit ([7523f3a](https://github.com/nymphanamusic/ksem-transformer/commit/7523f3a210055d0eff8efc12b285e96351efea86))
* ✨ add `deep_join_trees` ([882b7ce](https://github.com/nymphanamusic/ksem-transformer/commit/882b7cee2613e9b160d2308b934ed814e568bc13))
* ✨ add `store-pitch-range-setting-in` option ([988220f](https://github.com/nymphanamusic/ksem-transformer/commit/988220f06bc0d6c3dc7a98c73bc28f19e7b2bc84))
* ✨ add `to_yaml` method ([dcd6f83](https://github.com/nymphanamusic/ksem-transformer/commit/dcd6f838e91db438aae70a5ad17db8ba7b4f9d13))
* ✨ add `to-ksem` and `from-ksem` commands ([ad75c3d](https://github.com/nymphanamusic/ksem-transformer/commit/ad75c3d16cb0424d15a1d4040d8a415813be365c))
* ✨ add more complete model dumping ([c8dc075](https://github.com/nymphanamusic/ksem-transformer/commit/c8dc075d7a86a32d2d60c1083fcb8429b6397a50))
* ✨ add parsing and better dumping ([4343d7b](https://github.com/nymphanamusic/ksem-transformer/commit/4343d7b1b5daa27cdcd09ccd59dd43b971516b9e))
* ✨ add root_octave generation & fix notes having octaves ([7d0b6dd](https://github.com/nymphanamusic/ksem-transformer/commit/7d0b6ddbad035d092b131bc1aba27768fbaeca09))
* ✨ add serializer ([8516113](https://github.com/nymphanamusic/ksem-transformer/commit/8516113ddbc509ec8eacfa606ee084d19909bd33))
* ✨ allow merging converted YAML into an existing file ([16e233c](https://github.com/nymphanamusic/ksem-transformer/commit/16e233c06b23f040ee65775a9ff5498d921ba81a))
* ✨ allow user to specify where to store the YAML settings ([7159410](https://github.com/nymphanamusic/ksem-transformer/commit/71594106951c02edca65e6a850e30650a1948fed))
* ✨ load settings from KSEM configs ([de18194](https://github.com/nymphanamusic/ksem-transformer/commit/de181941c50ac64d71848f504c216370cf772439))
* ✨ make Note hashable & add comparison methods ([19195d1](https://github.com/nymphanamusic/ksem-transformer/commit/19195d1ae88fdd353ddbf8cfa5dff8fc39412182))
* add build-binary.yml ([d9d3d34](https://github.com/nymphanamusic/ksem-transformer/commit/d9d3d3430df8f40d635f1d9e6595b855d0b7ce46))


### Bug Fixes

* :adhesive_bandage: fix incorrect KSEM option selection ([938c9ac](https://github.com/nymphanamusic/ksem-transformer/commit/938c9ac56707eeb49b77baec9b4747805f120ae4))
* :bug: fix arbitrary type not being allowed ([a5fc825](https://github.com/nymphanamusic/ksem-transformer/commit/a5fc8255606c013b027071445900af924a5333f1))
* :bug: fix incorrect image to text transcription ([f0cf8d6](https://github.com/nymphanamusic/ksem-transformer/commit/f0cf8d6dd80ffa203ffe470ac668e7b21ca10187))
* 🐛 add files I forgot to stage ([e4210fc](https://github.com/nymphanamusic/ksem-transformer/commit/e4210fc35a5c6304e1186ded3cbbd530b270f98a))
* 🐛 fix circular model field ([f79b54a](https://github.com/nymphanamusic/ksem-transformer/commit/f79b54ac1bcd12239bd8f3ccfffd45284adeb487))
* 🐛 fix color not being serialized to list ([dc666bd](https://github.com/nymphanamusic/ksem-transformer/commit/dc666bdf4397fc8c0c32ae1bff2e16d86ab609a8))
* 🐛 fix forgetting to lock Poetry ([f7d9e24](https://github.com/nymphanamusic/ksem-transformer/commit/f7d9e243e1963a6b36009285efdfc3431a97843b))
* 🐛 fix from_midi not using middle_c properly ([a847ac1](https://github.com/nymphanamusic/ksem-transformer/commit/a847ac1a119d802415a6af335dca552e1522494b))
* 🐛 fix inconsistent `type` keyword usage ([efcbff8](https://github.com/nymphanamusic/ksem-transformer/commit/efcbff816c76e4c686b72d746c8b42048e50b33f))
* 🐛 fix nested `with_middle_c`s not recovering past values ([03c12d8](https://github.com/nymphanamusic/ksem-transformer/commit/03c12d8e4512a6de2910dcd44926d635e60132bd))
* 🐛 fix validators using ChildDict not properly loading nested data ([b412698](https://github.com/nymphanamusic/ksem-transformer/commit/b4126988135b6f5880ac013e18b9662a8b1dae1a))
* 🐛 fix YAML load deprecation ([4e07527](https://github.com/nymphanamusic/ksem-transformer/commit/4e07527dd1bdbac137ba76b319ed18b7a82562f1))
* 🩹 fix incorrect field type ([aa71f68](https://github.com/nymphanamusic/ksem-transformer/commit/aa71f685a0954a10908e3a31384bc203be7cbdca))
* 🩹 fix Notes not being made aware of middle C ([f193122](https://github.com/nymphanamusic/ksem-transformer/commit/f1931226d6799a81960d8104c5f1888fdeace819))


### Documentation

* :bulb: add docstrings and comments ([b1325eb](https://github.com/nymphanamusic/ksem-transformer/commit/b1325eb3850816bc036562b288d0be1c759f8f3a))
* 📄 add license ([b93995f](https://github.com/nymphanamusic/ksem-transformer/commit/b93995fa658d87c5ec041fb2f098a5ad8afad8dc))


### Code Refactoring

* 🚚 clarify MIDI control names ([223cb17](https://github.com/nymphanamusic/ksem-transformer/commit/223cb17609212a640bfb466f8d944372f6d3e219))
