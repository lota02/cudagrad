from os import environ, system
from pathlib import Path
from pstats import Stats
from textwrap import dedent

README = f"""\
<div align="center">
<h1>
    <div>cudagrad</div>
</h1>

CUDA C++ strided float tensor automatic differentiation engine with Python bindings

</div>

# Install

```
pip install cudagrad
```

# Examples

The following examples were written purely in Python using only [`cudagrad.Tensor`](./Tensor.ipynb) for learning:

"""


def compare(c: float, t: float) -> str:
    if t == 0:
        raise ValueError
    return ((c - t) / t) * 100

def profile(examples: list[str]):
    global README
    
    for example in examples:
        # system(f"python -m cProfile -o ./benchmarks/_cudagrad/profiles/{example}.prof ./benchmarks/_cudagrad/{example}.py")
        # system(f"python -m cProfile -o ./benchmarks/_torch/profiles/{example}.prof ./benchmarks/_torch/{example}.py")
        t = Stats(f"./benchmarks/_torch/profiles/{example}.prof")
        c = Stats(f"./benchmarks/_cudagrad/profiles/{example}.prof")
        README = README + dedent(f"""\

### {example.upper()}

![](benchmarks/_cudagrad/plots/{example}.jpg)

[`/benchmarks/_cudagrad/{example}.py`](https://github.com/yrmo/cudagrad/blob/main/benchmarks/_cudagrad/{example}.py) ({compare(c.total_tt, t.total_tt):+}% {"faster" if c.total_tt <= t.total_tt else "slower"} than `torch`)

""")


if __name__ == "__main__":
    environ["PROFILING"] = "1"
    profile([x.stem for x in list(Path('.').glob('./benchmarks/_torch/*.py'))])

    with open("README.md", "w") as f:
        f.write(README)
