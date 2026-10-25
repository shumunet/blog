---
title: "AtCoder Beginner Contest 481 游记"
description: "整理 AtCoder Beginner Contest 481 的赛时解题，包含题意、解题思路与代码实现。"
cover: /img/covers/acg-005.jpg
date: 2026-10-24 22:00:00
categories:
  - 算法竞赛
tags:
  - AtCoder
math: true
---

## 赛时状况

E 题是个计算几何，直接扔了，我又不可能撕咬 G 题，过了 D 之后就去看 F 了，看到 F 是个图论题就仔细想了想，发现是个还挺经典的思路，想了想成功过掉了，捡漏拿下 5 题。

## A - Digits of A+B

### 题意简述

给你两个一位数，判断这两个数和是几位数。

### 题解

注意到只能是一位数或者两位数，判断即可。

```c++
void solve() {
    int a,b;
    cin>>a>>b;
    if(a+b>=10) cout<<2;
    else cout<<1;
}
```

## 			B - Polyline 		 	

### 题意简述

给你 $N$ 个平面直角坐标系上的点，对于第 $i$ 个点，横坐标是 $i$，纵坐标是输入的（保证第 $i$ 个点的纵坐标不等于第 $i-1$ 个点的），把第 $i$ 个点和第 $i-1$ 个点连接，形成一条折线，问这个折线上有多少个纵坐标为 $k$ 的点。

### 题解

画图画画样例，然后因为两个点之间的直线肯定单调，然后就判定一下就做完了。

```c++
void solve() {
    int n,k;
    cin>>n>>k;
    int ans=0;
    vector<int>a(n+1);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
        if(a[i]==k) {
            ans++;
            continue;
        }
        if(i==1) continue;
        if((a[i]>k&&a[i-1]<k)||(a[i]<k&&a[i-1]>k)) ans++;
    }
    cout<<ans;
}
```

## 			C - Bank Accounts 		 	

### 题意简述

依次处理南瓜的名字：若该名字已有账户，输出其ID；否则为其分配当前最小未使用的正整数ID并输出。

### 题解

就是哈希表模板题，这里我们使用 `map` 直接秒了。

```c++
void solve() {
    int q;
    cin>>q;
    int id=0;
    map<string,int> mp;
    while(q--) {
        string s;
        cin>>s;
        if(mp[s]) {
            cout<<mp[s]<<endl;
        }
        else {
            mp[s]=++id;
            cout<<mp[s]<<endl;
        }
    }
}
```

## 			D - Autopilot

### 题意简述 		 	

给一个 $N$ 个点 $M$ 条边的有向图，每条边边权是 1，另外，对于点 $u$，还额外有一条边权是 0 的边连向它能到达的最小编号的点，问点 $s$ 到点 $t$ 的最短路。

### 题解

> 图论题好耶～

读完题感觉就是建图跑 `dijkstra` 就解决了，对于边权为 0 的边这个问题显然可以直接维护一个数组解决。但是后面发现有点没必要，边权 1 或者 0，这不是直接 `01-bfs` 就行了吗（其实 `01-bfs` 是 `dijkstra` 算法的特殊情况，可以用双端队列代替优先队列来加速），启动！

```c++
int n,m,s,t;
int mn[MAXN];
int dis[MAXN];
vector<int> edge[MAXN];
deque<pair<int,int>> que;
void solve() {
    cin>>n>>m>>s>>t;
    memset(mn,0x3f,sizeof(mn));
    for(int i=1;i<=m;i++) {
        int u,v;
        cin>>u>>v;
        edge[u].push_back(v);
        mn[u]=min(mn[u],v);
    }
    memset(dis,0x3f,sizeof(dis));
    dis[s]=0;
    que.push_front({s,0});
    while(!que.empty()) {
        int u=que.front().first;
        int d=que.front().second;
        que.pop_front();
        if(d!=dis[u]) continue;
        for(int v:edge[u]) {
            int w=(v==mn[u]?0:1);
            if(dis[v]<=d+w) continue;
            dis[v]=d+w;
            if(w==0) que.push_front({v,dis[v]});
            else que.push_back({v,dis[v]});
        }
    }
    if(dis[t]==0x3f3f3f3f) cout<<-1;
    else cout<<dis[t];
}
```

## 			F - Evil Shortest Path 		 	

### 题意简述

给定一个有向图，包含 $N$ 个顶点和 $M$ 条边，顶点编号为 $1$ 到 $N$。每条边从一个顶点指向另一个顶点，并标有一个 $1$ 到 $9$ 之间的数字。

从顶点 $1$ 出发，沿有向边走到某个顶点。把经过的边上的数字按照经过顺序依次拼接起来，得到一个整数，称为这条路径对应的分数。路径中允许重复经过顶点和边。

对于每个顶点 $v$（$2 ≤ v ≤ N$），求从顶点 $1$ 到 $v$ 的所有路径中，分数最小的那一个，并输出该分数对 `998244353` 取模后的结果。题目保证从顶点 $1$ 可以到达所有其他顶点。

### 题解

容易注意到，当前分数 $x$ 的话，我走一条 $c$ 的边，分数变为 $10x+c$，这击破了我本来想分层图来做的想法。但是，这启发我可以使用 `BFS` 求出 $1$ 号点到达每个点走的最少的边数，因为显然走的边数少的才能是分数最小的候选结果。接下来，就是思考如何处理走的边一样的前提下最小化分数了。

这个问题可以用反向建图维护前缀路径来解决，这里一开始的想法是字符串模拟，因为本质就是比字典序，但是注意到数据范围比较恐怖，可能会 MLE。好在最后我想到了一种维护方式：维护每个字符串对应的排名，这样就省下来内存了，而且比较的代价也更小了，就可以通过本题了。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 998244353;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'
#define int long long

vector<pair<int,int>> edge[MAXN];
vector<pair<int,int>> redge[MAXN];
int n,m,md;
int d[MAXN];
int p[MAXN],c[MAXN];
queue<pair<int,int>> que;
bool vis[MAXN];

bool cmp(int a,int b) {
    return pair<int,int>{p[a],c[a]}<pair<int,int>{p[b],c[b]};
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n>>m;
    for(int i=1;i<=n;i++) d[i]=INF;
    for(int i=1;i<=m;i++) {
        int u,v,w;
        cin>>u>>v>>w;
        edge[u].push_back({v,w});
        redge[v].push_back({u,w});
    }
    que.push({1,0});
    vis[1]=true;
    d[1]=0;
    while(!que.empty()) {
        int step=que.front().second;
        int u=que.front().first;
        que.pop();
        for(auto [v,w]:edge[u]) {
            if(vis[v]) continue;
            vis[v]=true;
            d[v]=step+1;
            que.push({v,step+1});
        }
    }
    for(int i=1;i<=n;i++) {
        md=max(md,d[i]);
    }
    vector<vector<int>> layer(md+1);
    for(int i=1;i<=n;i++) {
        layer[d[i]].push_back(i);
    }
    vector<int> r(n+1,-1),ans(n+1,0);
    r[1]=0;
    for(int dep=1;dep<=md;dep++) {
        for(int i=0;i<(int)layer[dep].size();i++) {
            int v=layer[dep][i];
            int br=INF,bc=INF,bp=-1;
            for(auto [u,w]:redge[v]) {
                if(d[u]!=dep-1) continue;
                if(pair<int,int>{r[u],w}<pair<int,int>{br,bc}) {
                    br=r[u];
                    bc=w;
                    bp=u;
                }
            }
            p[v]=br;
            c[v]=bc;
            ans[v]=(ans[bp]*10+bc)%MOD;
        }
        vector<int> ord=layer[dep];
        sort(ord.begin(),ord.end(),cmp);
        int now=0;
        for(int i=0;i<(int)ord.size();i++) {
            if(i>0) {
                int a=ord[i-1],b=ord[i];
                if(pair<int,int>{p[a],c[a]}!=pair<int,int>{p[b],c[b]}) now++;
            }
            r[ord[i]]=now;
        }
    }
    for(int i=2;i<=n;i++) {
        cout<<ans[i]<<endl;
    }
    return 0;
}
```

