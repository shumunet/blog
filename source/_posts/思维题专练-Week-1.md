---
title: "思维题专练 Week 1"
description: "整理七道思维与构造题，涉及数论、字符串、矩阵及图的构造方法。"
cover: /img/covers/anime-09.webp
date: 2026-10-11 23:00:00
categories:
  - 算法竞赛
tags:
  - 构造
  - 专项练习
math: true

---

## 前言

因为本人的构造能力实在是有点太唐了，所以我从 10 月 6 日开始打算每天刷一些思维题提升提升能力，这是第一周做的题目。

## P17620 [qaswed12 OI R1] Bot Problem

### 题意简述

多组询问，每组询问给定一个正整数 $a$，请构造三元组 $(b,c,d)$ 满足：
- $ab+cd=\text{lcm}(a,c)+\text{lcm}(b,d).$
- $b \ne c.$
- $b,c,d$ 为正整数。

你需要输出 $b,c,d$ 的值。

### 题解

看到这种形式，我们应该进行一些大胆猜测，这里我们猜测

$ab = \text{lcm}(b,d)$

$cd = \text{lcm}(a,c)$

对于 $ab = \text{lcm}(b,d)$ ，我们可以令 $b = 1$ 和 $d = a$ 来完成它，我们代入第二项，得到：

$ac = \text{lcm}(a,c)$

由于：

$\text{lcm}(a,c) = \frac{ac}{\text{gcd}(a,c)}$

$\implies \text{lcm}(a,c) = 1$

所以需要 $a$ 和 $c$ 互素，我们直接令 $c = a + 1$ 或者 $c = a-1$ ，这道题就做完了。

```c++
void solve() {
    int a;
    cin>>a;
    if(a<=2) {
        cout<<1<<" "<<a+1<<" "<<a;
    }
    else {
        cout<<1<<" "<<a-1<<" "<<a;
    }
    cout<<endl;
}
```

## P15655 [ICPC 2025 Jakarta R] Nihilation

### 题意简述

给定一个由 $N$ 个正整数组成的数组 $A = [A_1, A_2, \ldots, A_N]$。

在一次操作中，你可以选择整数 $m$ 和 $k$，满足 $1 \leq k < m \leq 10^9$，并对所有 $1 \leq i \leq N$ 将 $A_i$ 设置为 $(A_i \times k) \bmod m$。

问最少需要多少次操作才能使所有 $A_i$ 都变为 $0$？

输出任意一种可行的操作序列。可以证明，总是有可能使所有 $A_i$ 变为 $0$。

### 题解

首先，我们想一想操作次数的上限是什么。

容易注意到：**所有 2 的倍数对 2 取模得到的结果一定是 0**

那就容易得到最多只有 2 次操作，接下来就是想一想怎么构造了。

如果这个数组不互素的话，那么只需要取余它们的最大公约数就一定可以全部归零了，因为本来都是它们最大公约数的倍数。

如果这个数组互素的话，那么我们可以通过乘偶数再取余偶数的方式，让所有的数都变成偶数，接下来只要对 2 取模就得到 0 了。

**Trick：利用模运算制造一个统一的素因子。**

```c++
int gcd(int a,int b) {
    if(b==0) return a;
    return gcd(b,a%b);
}
void solve() {
    int n;
    cin>>n;
    int g;
    cin>>g;
    for(int i=1;i<n;i++) {
        int x;
        cin>>x;
        g=gcd(x,g);
    }
    if(g==1) {
        cout<<2<<endl;
        cout<<12<<" "<<6<<endl;
        cout<<2<<" "<<1;
    }
    else {
        cout<<1<<endl;
        cout<<g<<" "<<1;
    }
}
```

## CF805B 3-palindrome

### 题意简述

给定n，求长度为n的以'a','b'或'c'构成的字符串，使得其中不存在长为 3 的回文子串（如"abc","abca"均符合，但"aba"不符），并使'c'的个数尽可能少

### 题解

被骗了，一开始以为结论是 `baabcabcabc...` 这种，结果发现只要是 `aabb` 循环就不可能有长度为 3 的回文子串。

```c++
void solve() {
    int n;
    cin>>n;
    string s="aabb";
    for(int i=0;i<n;i++) {
        cout<<s[i%4];
    }
}
```

## CF743C Vladik and fractions

### 题意简述

给定 $n$，请找出三个不同的正整数 $x$、$y$、$z$，使得 $\frac{2}{n} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}$。由于 Chloe 无法验证太大的数，所以需保证所有的数都不超过 $10^9$。

如果不存在这样的答案，请输出 $-1$。

### 题解

直接令 $z = n$ ，那么有 $\frac{1}{x} +\frac{1}{y} = \frac{1}{n}$ 。

对 $\frac{1}{n}$ 进行裂项，得到 $\frac{1}{n} = \frac{1}{n(n+1)} + \frac{1}{n+1}$

那就简单了，直接令 $x = n(n+1)$ $y = n + 1$

什么时候无解呢？显然只有 $n \leq 1$ 的时候无解。

```c++
void solve() {
    ll n;
    cin>>n;
    if(n<=1) cout<<-1;
    else cout<<n*(n+1)<<" "<<n+1<<" "<<n;
}
```

## CF1708B Difference of GCDs

### 题意简述

给定三个整数 $n$、$l$ 和 $r$。你需要构造一个数组 $a_1,a_2,\dots,a_n$，满足 $l\le a_i\le r$，并且 $\gcd(i,a_i)$ 两两互不相同。如果无法构造出这样的数组，则输出无解。

### 题解

显然 $\text{gcd}(i,a_i) = i$，证明很好证明，因为 $\text{gcd}(i,a_i)$ 的取值范围是 $[1,i]$ 而 $[1,i-1]$ 都被用过了。

那么接下来就是令 $a_i = ki$，最大的 $k = \lfloor \frac{r}{i} \rfloor$。

所以很简单，直接令 $ans_i = \lfloor \frac{r}{i} \rfloor n$，如果 $ans_i \lt l$ 就无解。

```c++
void solve() {
    ll n,l,r;
    cin>>n>>l>>r;
    vector<ll>ans;
    bool flag=true;
    for(int i=1;i<=n;i++) {
        //cout<<(r/i)*i<<" ";
        ans.push_back((r/i)*i);
        if((r/i)*i<l) {
            flag=false;
        }
    }
    if(flag) {
        cout<<"YES"<<endl;
        for(int v:ans) cout<<v<<" ";
        cout<<endl;
    }
    else {
        cout<<"NO"<<endl;
    }
}
```

## P7873 「SWTR-7」Scores（easy version）

### 题意简述

试构造一个 $n\times m$ 的矩阵 $s$，满足所有元素为 $[0,100]$ 之间的整数，且对于任意 $i,j\ (i\neq j)$ 存在一个 $k$ 使得 $s_{i,k}>s_{j,k}$。

### 题解

这个很容易注意到当且仅当 $m = 1$ 且 $n > 1$ 的时候无解，因为这个时候不可能存在 $k$ 。

接下来考虑怎么构造，其实我们可以选两列，一个单调递增，一个单调递减，这样就一定符合了。

```c++
int ans[MAXN][MAXN];
void solve() {
    int n,m;
    cin>>n>>m;
    for(int i=1;i<=n;i++) {
        for(int j=1;j<=m;j++) {
            ans[i][j]=0;
        }
    }
    if(m==1&&n>1) {
        cout<<"NO"<<endl;
        return;
    }
    cout<<"YES"<<endl;
    for(int j=1;j<=n;j++) ans[j][1]=j;
    for(int j=1;j<=n;j++) ans[j][2]=n-j+1;
    for(int i=1;i<=n;i++) {
        for(int j=1;j<=m;j++) {
            cout<<ans[i][j]<<" ";
        }
        cout<<endl;
    }
}
```

## CF1581B Diameter of Graph

### 题意简述

问能否构造出 $n$ 个节点 $m$ 条边且直径严格小于 $k-1$ 的无向连通图，要求没有重边和自环。

### 题解

一开始想了个错误的构造：先用 $n-1$ 条边连起来构成一个链，然后我把最远的两个点连接直到直径小于 $k-1$，然后看有没有剩下的边，但是我没想到的是可以直接构造**星形图**。

```
          2   3   4
           \  |  /
      5 ———— 1 ———— 6
           / | \ \
          7  8  9  10
```

这样就结束了。

```c++
void solve() {
    ll n, m, k;
    cin >> n >> m >> k;

    ll mx = n * (n - 1) / 2;
    if(m < n - 1 || m > mx) {
        cout << "NO" << endl;
        return;
    }

    int d;
    if(n == 1) d = 0;
    else if(m == mx) d = 1;
    else d = 2;

    cout << (d < k - 1 ? "YES" : "NO") << endl;
}
```

