---
title: "Codeforces Round 1123 (Div. 2) 补题"
description: "整理 XOR Transformations 的简单版与困难版，介绍异或变换的收敛性质及 01 Trie 与堆的优化思路。"
cover: /img/covers/anime-04.webp
date: 2026-09-26 18:00:00
categories:
  - 算法竞赛
tags:
  - Codeforces
math: true
---

## 补题复盘

比赛过程中写完 D 题发现不会 E 题就跑路了，虽然 F1 题明显通过率更高，但是也没有去玩它的性质，不然应该能切出来的，痛失了直接到达 1400 分的机会 T_T

## F1. XOR Transformations (Easy Version) 

### 题意简述

给定一个长度为 $n$ 的非负整数数组 $a$。

每次操作，计算所有 $i<j$ 的 $a_i\oplus a_j$，从这 $\binom n2$ 个结果中选出最小的 $n$ 个，组成新数组。重复值按出现次数保留。

有 $q$ 个独立询问，每次给定 $x$，求原数组经过 $x$ 次操作后的最大值与最小值之差。

### 题解

手玩样例，注意到这个东西收敛极快，经过几次变化之后就变成全 $0$ 了，那答案显然就是 $0$ 了，直接暴力预处理即可，时间复杂度比较神秘，但是实际上跑的飞快。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n,q;
    cin>>n>>q;
    vector<int> a(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
    }
    vector<int> ans(MAXN,0);
    ans[0]=*max_element(a.begin()+1,a.end())-*min_element(a.begin()+1,a.end());
    priority_queue<int> que;
    int cnt=0;
    while(1) {
        for(int i=1;i<=n;i++) {
            for(int j=i+1;j<=n;j++) {
                que.push(a[i]^a[j]);
                if(que.size()>n) que.pop();
            }
        }
        for(int i=1;i<=n;i++) {
            a[i]=que.top();
            que.pop();
        }
        ans[++cnt]=abs(a[1]-a[n]);
        if(a[1]==0) break;
    }
    while(q--) {
        int x;
        cin>>x;
        if(x>cnt) {
            cout<<0<<endl;
        }
        else {
            cout<<ans[x]<<endl;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    cin>>T;
    while (T--) {
        solve();
    }
    return 0;
}

```

## F2. XOR Transformations (Hard Version)

### 题意简述

与本题的简单版本一致，不同的是 $n$ 和 $q$ 的范围来到了恐怖的 $1e5$。

### 题解

根据刚刚我们注意到的结果，其实 $q$ 的增长是影响不大的，因为确实收敛很快，我们查询是很容易就能做到的，唯一不同的是因为 $n$ 增长了，我们没办法再暴力预处理了，得需要想办法优化。

那我们怎么优化呢？这里想到了之前学到的数据结构：**01 trie**，这个东西可以快速处理出最小的异或值，接下来就是怎么维护第 k 小了，这玩意似乎和权值线段树的思想类似，那我们就可以把一次变换从暴力的 $O(n^2\log n)$，降到了 $O(n(B+\log n))$。

套进去看看，结合小根堆维护一下似乎就可以过了。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MAXN = 2e5+100;
#define endl '\n'

int trie[MAXN*31][2],sz[MAXN*31],tot=1;

void clear() {
    for(int i=1;i<=tot;i++) {
        trie[i][0]=trie[i][1]=sz[i]=0;
    }
    tot=1;
}

void insert(int x,int v) {
    int p=1;
    sz[p]+=v;
    for(int i=30;i>=0;i--) {
        int ch=(x>>i)&1;
        if(trie[p][ch]==0) {
            trie[p][ch]=++tot;
        }
        p=trie[p][ch];
        sz[p]+=v;
    }
}

int get_ans(int x,int k) {
    insert(x,-1);

    int p=1,ans=0;
    for(int i=30;i>=0;i--) {
        int ch=(x>>i)&1;
        int s=sz[trie[p][ch]];

        if(k<=s) {
            p=trie[p][ch];
        }
        else {
            k-=s;
            ans+=(1<<i);
            p=trie[p][ch^1];
        }
    }

    insert(x,1);
    return ans;
}

struct node {
    int val,id,k;

    bool operator < (const node &b) const {
        return val>b.val;
    }
};

void solve() {
    int n,q;
    cin>>n>>q;

    vector<int> a(n+1,0),b(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
    }

    vector<int> ans;
    ans.push_back(
        *max_element(a.begin()+1,a.end())
        -*min_element(a.begin()+1,a.end())
    );

    int cnt=0;
    while(*max_element(a.begin()+1,a.end())>0) {
        clear();
        for(int i=1;i<=n;i++) {
            insert(a[i],1);
        }

        priority_queue<node> que;
        for(int i=1;i<=n;i++) {
            que.push({get_ans(a[i],1),i,1});
        }

        for(int i=1;i<=2*n;i++) {
            node t=que.top();
            que.pop();

            if(i%2==0) {
                b[i/2]=t.val;
            }

            if(i<2*n && t.k<n-1) {
                que.push({
                    get_ans(a[t.id],t.k+1),
                    t.id,
                    t.k+1
                });
            }
        }

        for(int i=1;i<=n;i++) {
            a[i]=b[i];
        }

        ans.push_back(a[n]-a[1]);
        cnt++;
    }

    while(q--) {
        ll x;
        cin>>x;
        if(x>cnt) {
            cout<<0<<endl;
        }
        else {
            cout<<ans[x]<<endl;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T=1;
    cin>>T;
    while(T--) {
        solve();
    }
    return 0;
}
```
