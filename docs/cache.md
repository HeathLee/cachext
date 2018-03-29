# cachext.exts.Cache

## 相关配置

`CACHE_BACKEND`

> Cache 的实现，目前有：`Simple` 和 `Redis`

`CACHE_PREFIX`

> cache 中 key 的前缀，默认为 `app.name`

`CACHE_DEFAULT_TTL`

> 默认的 ttl， 默认值为 172800

`CACHE_*`

> 其他配置，会作为字典参数传递给 backend

**注意：`CACHE_` 为默认的配置前缀，可以在初始化 Cache对象时通过指定 `ns` 参数改变。例如：**

```python
cache = cachext.exts.Cache(ns='XXX_')
```

会读取： `XXX_BACKEND`, `XXX_PREFIX` 等配置。


## 支持的命令

`get`, `get_many`, `set`, `set_many`, `delete`, `delete_many`, `expire`, `expireat`, `clear`, `ttl`, `exists`


## Cache.cached

`Cache.cached(func=None, ttl=None, cache_key=cachext.cache.default_key, unless=None, fallbacked=None, cache_none=False)`

**被 cached 装饰后，当函数被调用时，先去查缓存，如果有结果(缓存命中)，就会直接返回缓存的结果。如果没有结果(缓存未命中)，就会调用原函数重新计算结果，并将结果写入缓存，然后返回结果。**

可以直接作为装饰器，也可以接受参数，初始化后再作为装饰器使用。例如：

```python
from app.extensions import cache

@cache.cached(ttl=60)
def f():
    pass
```

#### `ttl`

缓存的ttl，类型为`int`，单位为 "秒"

默认值为config中的 `CACHE_DEFAULT_TTL`

#### `cache_key`

缓存的key。可以是`string`，也可以是一个 `callable` 的对象。

当传入的是一个 `callable` 对像时，会每次发生调用时， 调用`cache_key(f, *args, **kwargs)` 来生成缓存的 key。
其中 `f` 为原函数，`*args`, `**kwargs` 为调用参数。

默认值 `cachext.cache.default_key` 定义如下：

```python
def default_key(f, *args, **kwargs):
    keys = [norm_cache_key(v) for v in args]
    keys += sorted(
        ['{}={}'.format(k, norm_cache_key(v)) for k, v in kwargs.items()])
    return 'default.{}.{}.{}'.format(f.__module__, f.__name__, '.'.join(keys))
```

#### `unless`

为一个 `callable` 的对象，返回值为 `True` 或者 `False`，当返回 `True` 的时候，直接调用原函数，而不走缓存。
如果 `unless` 不是 `callable` 对象，则相当于总是返回 `False`

每次发生调用时，会调用 `unless(*args, **kwargs)` 获取返回值， 其中`*args`, `**kwargs` 为调用参数。


#### `fallbacked`

为一个 `callable` 的对象，每次缓存没有命中，而调用到原函数时，会被调用。如果 `fallbacked` 不是 `callable` 的，则不会有任何效果

其调用参数为：`fallbacked(wrapper, rv, *args, **kwargs)`，其中 `wrapper` 为被装饰后的函数，`rv` 为原函数的返回值


#### `cache_none`

是否缓存 `None`，类型为 `bool`。如果为`True`，那么当原函数返回`None`，也会被缓存。并且下次调用不会 fallback 到原函数。
