---
title: "Hash Length Extension Attack 学习笔记"
description: "介绍 MD5 的处理流程、哈希长度扩展攻击的原理，以及 HashPump 的使用方法。"
cover: /img/covers/anime-05.webp
date: 2026-09-28 14:00:00
categories:
  - 网络安全
tags:
  - 学习笔记
  - Crypto
math: true
---

## 前言

**Hash Length Extension Attack** 是针对 **[Merkle–Damgård 结构](https://en.wikipedia.org/wiki/Merkle–Damgård_construction)** 的哈希函数攻击手段，可以用于攻击 `md5` `SHA-1` `SHA-2` 等哈希算法。该攻击手段可以伪造消息散列值，产生合法的数字签名。

本文将会以 `md5` 为例，介绍该攻击手段的基本原理以及攻击方法。

## MD5 流程

### 概括

把消息分成若干块，用每一块不断更新一个 128 位内部状态，最后把这个状态输出为摘要。

### 填充与分块

对于长度为 $L$ 位的信息：

- 先追加一个 `1` 位，用于标记填充开始
- 再追加若干个 `0` 位，使得长度对 $512$ 取模为 $448$
- 最后追加一个 $64$ 位整数，记录原始长度 $L\bmod 2^{64}$，采用小端序

这样消息长度就是 512 位的整数倍。每块 512 位，即 64 字节，再拆成 16 个 32 位整数 `M[0..15]`。

### 初始化

状态由四个 32 位整数构成，初值固定：

```
A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476
```

### 每个块进行 $64$ 步混合

分成 $4$ 轮，没轮 $16$ 步，分别使用以下函数：

```
F(B,C,D) = (B & C) | (~B & D)
G(B,C,D) = (B & D) | (C & ~D)
H(B,C,D) = B ^ C ^ D
I(B,C,D) = C ^ (B | ~D)
```

每一轮可以概括为下面的过程：

```
T = B + 循环左移(A + 本轮函数(B,C,D) + M[k] + K[i], s)
(A, B, C, D) = (D, T, B, C)
```

这里：

- `M[k]` 是按规定顺序选取的消息字；
- `K[i]` 是固定常量；
- `s` 是规定的移位数；
- 所有加法都只保留低 32 位，即模 $2^{32}$ 加法。

这些运算反复混合消息和状态，使输入的变化扩散到输出的各个位。

### 合并状态进入下一块

处理一块前，先保存状态 `(A₀,B₀,C₀,D₀)`。64 步结束后，逐项相加：

```
A = A + A₀
B = B + B₀
C = C + C₀
D = D + D₀
```

同样只保留低 $32$ 位。

### 输出摘要

把最终的 `A、B、C、D` 分别按小端序编码并拼接，得到 **16 字节，即 128 位**的摘要，通常显示为 32 个十六进制字符。

## MD5 扩展长度攻击

根据刚刚对 `md5` 的学习，我们容易发现 `md5` 最终摘要的本质其实就是处理完所有块后的内部状态。

如果攻击者知道如下内容：

```
MD5(secret || message)
```

那么这个 $128$ 位的摘要就暴露了处理 `secret || message` 后的内部状态。攻击者就可以根据已知的 `message` 的长度算出填充长度，然后把摘要中的状态作为初始状态，往后追加内容，得到：

```
MD5(secret || message || padding || extra)
```

## HashPump 漏洞利用

```
HashPump [-h help] [-t test] [-s signature] [-d data] [-a additional] [-k keylength]
     HashPump generates strings to exploit signatures vulnerable to the Hash Length Extension Attack.
     -h --help          Display this message.
     -t --test          Run tests to verify each algorithm is operating properly.
     -s --signature     The signature from known message.
     -d --data          The data from the known message.
     -a --additional    The information you would like to add to the known message.
     -k --keylength     The length in bytes of the key being used to sign the original message with.
```

