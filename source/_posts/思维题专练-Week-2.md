---
title: "思维题专练 Week 2"
description: "整理区间翻转、最大异或对与数组合并等思维题的解题思路，部分题解仍待补充。"
cover: /img/covers/anime-10.webp
date: 2026-10-18 20:00:00
categories:
  - 算法竞赛
tags:
  - 构造
  - 专项练习
math: true

---

## 前言

因为本人的构造能力实在是有点太唐了，所以我打算刷一些思维题提升提升能力，这是第二个专题周周做的题目。（其实这周完全没做啥啊233，一直在准备月考x）

## CF2217B Flip the Bit (Easy Version)

### 题目描述

给定一个只有 0 和 1 组成的数组和一个特殊下标，每次操作可以选择一个包含了特殊下标的区间，使这个区间里面的所有数取反，问最小多少次操作可以把所有数都变成特殊下标的原始值。

### 题解

考虑简单的贪心，我们维护两个指针，一个左指针永远向右，右指针永远向左，只要是没变对就让这个区间翻转，然后注意到我们不需要真的翻转，只需要维护翻转次数，因为翻转两次就等于没翻转。

```c++
void solve() {
    int n,k;
    cin>>n>>k;
    vector<int> a(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
    }
    int p;
    cin>>p;
    int ans=0;
    int l=1,r=n;
    while(l!=r) {
        while(l<p&&a[l]==(a[p]^(ans&1))) l++;
        while(r>p&&a[r]==(a[p]^(ans&1))) r--;
        //cout<<l<<" "<<r<<endl;
        ans++;
    }
    if(ans&1) ans--;
    cout<<ans<<endl;
}
```

## CF2218E The 67th XOR Problem

### 题意简述

给定一个初始包含 $n$ 个非负整数的数组 $a$。
你需要恰好执行 $n−1$ 次如下操作：
1. 选择数组的一个下标 $i$（$1 \le i \le |a|$，$|a|$ 为当前数组长度），记 $x = a_i$。
2. 对数组中所有下标 $j$（$1 \le j \le |a|$），令 $a_j = a_j \oplus x$（$\oplus$ 为按位异或）。
3. 从数组中删除 $a_i$。

可以证明，执行 $n−1$ 次操作后，数组中恰好只剩下一个元素。你的任务是：以最优方式选择操作顺序，使得最后剩下的元素尽可能大，并求出这个最大值。

### 题解

我们从简单状态开始进行一些模拟，假设数组有 3  个数字 $a,b,c$，我们选择了 $c$ 后数组剩下 $a \oplus c,b \oplus c$ 再选择 $b$ ，那么结果就变成了$(a \oplus c) \oplus (b \oplus c)$，展开观察到 $c$ 被异或了两次，也就是说被抵消掉了。所以我们不管怎么操作，最后的结果一定是原数组里面两个数的值，于是这道题就变成了最大异或对问题，显然可以 `01-trie` 解决。

```c++
int n,trie[MAXN][2],tot=1,a[MAXN];
void init() {
    memset(trie,0,sizeof(trie));
    tot=1;
}
void insert(int x) {
    int p=1;
    for(int i=30;i>=0;i--) {
        int ch=(x>>i)&1;
        if(trie[p][ch]==0) {
            trie[p][ch]=++tot;
        }
        p=trie[p][ch];
    }
}
int get_max(int x) {
    int p=1,ans=0;
    for(int i=30;i>=0;i--) {
        int ch=(x>>i)&1;
        if(trie[p][ch^1]) {
            ans+=1<<i;
            p=trie[p][ch^1];
        }
        else {
            p=trie[p][ch];
        }
    }
    return ans;
}
void solve() {
    init();
    cin>>n;
    for(int i=1;i<=n;i++) {
        int x;
        cin>>a[i];
        insert(a[i]);
    }
    int ans=-1;
    for(int i=1;i<=n;i++) {
        ans=max(get_max(a[i]),ans);
    }
    cout<<ans<<endl;
}
```

## CF2112B Shrinking Array

### 题意简述

序列 $b$ 是美丽的，当且仅当 $b$ 的长度至少为 $2$ 且存在一个位置 $i$ 使得 $\vert b_i-b_{i+1}\vert\le 1$。 

给你一个序列 $a$，你可以执行以下操作直到其长度少于 $2$。
- 选择 $a$ 中两个相邻的位置 $i$ 和 $i+1$。
- 选择一个整数 $x$ 使得 $\min(a_i,a_{i+1})\le x\le \max(a_i,a_{i+1})$。
- 删除 $a_i$ 和 $a_{i+1}$，并在它们的位置插入一个 $x$。这会使得 $a$ 的长度减少 $1$。

计算最少需要多少次操作使得 $a$ 变得美丽，或报告这是不可能的。

### 题解

这是一道诈骗题，看题解看出来的。关键在于**单调不美丽序列**一定不能通过操作变成美丽的（原因是我怎么去选我也没办法给他扩）。

如果不是单调不美丽序列，那么一定存在 $x,y,z$，其中 $y$ 是谷或顶，那么直接让它改成左边或者右边（总有能改的），就结束了。

所以答案只能是 $0,1,-1$。

```c++
void solve() {
    int n;
    cin>>n;
    vector<int> a(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
    }
    bool flag1=true,flag2=true,flag=false;
    for(int i=2;i<=n;i++) {
        if(abs(a[i]-a[i-1])<=1) flag=true;
    }
    if(flag) {
        cout<<0<<endl;
        return;
    }
    for(int i=2;i<=n;i++) {
        if(a[i]<a[i-1]) {
            flag1=false;
        }
    }
    for(int i=2;i<=n;i++) {
        if(a[i]>a[i-1]) {
            flag2=false;
        }
    }
    if(flag1||flag2) {
        cout<<-1<<endl;
    }
    else {
        cout<<1<<endl;
    }
}
```
