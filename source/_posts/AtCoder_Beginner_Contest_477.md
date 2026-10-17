---
title: "AtCoder Beginner Contest 477 游记"
description: "整理 AtCoder Beginner Contest 477 的 A 至 E 题，包含题意、解题思路与代码实现。"
cover: /img/covers/anime-02.webp
date: 2026-09-26 22:00:00
categories:
  - 算法竞赛
tags:
  - AtCoder
math: true
---

## 赛时状况

已经很长时间没打 ABC 了，这次 ABC 开到了 E 题，而且感觉其实 F 题也是可做的，也就是说我再训训没准能 AK？（下辈子估计可以）

## A - Traffic Light

### 题意简述

某个交通信号灯的颜色按 `B`（蓝色）、`Y`（黄色）、`R`（红色）、`B`（蓝色）、`Y`（黄色）、`R`（红色）、… 的顺序周期性变化。

给定一个字符 $c$，表示交通信号灯当前的颜色。输出交通信号灯的下一个颜色。

### 题解

显然，`B` 后面是 `Y`  ，`Y`  后面是 `R` ，`R` 后面是 `B` ，直接模拟就行。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    char c;
    cin>>c;
    if(c=='B') cout<<'Y';
    else if(c=='Y') cout<<'R';
    else cout<<'B';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    //cin>>T;
    while (T--) {
        solve();
    }
    return 0;
}

```

## 			B - Standing Outliers 		 	

### 题意简述

在数轴上有 $N$ 个人。这些人编号为 $1$ 到 $N$，第 $i$ 个人位于坐标 $X_i$。多个人可能位于同一坐标。

如果一个人到其他每个人的距离都至少为 $D$，则称其“与众不同”。

正式地说，如果对于所有 $j$（$1\le j\le N$，$j\ne i$）都有 $\lvert X_i-X_j\rvert\ge D$，则称第 $i$ 个人“与众不同”。

按升序输出所有“与众不同”的人的编号。

### 题解

我们考虑一个问题，如果这个人旁边的两个人离他的距离大于等于 $D$ ，那其他的人显然一定距离大于等于 $D$ 了，所以我们直接先排序，然后模拟就行了，不过这里要写个结构体，还要注意特殊处理最前面人的和最后面的人。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

struct NODE {
    int id,pos;
}a[MAXN];

bool cmp(NODE a,NODE b) {
    return a.pos>b.pos;
}
void solve() {
    int n,d;
    cin>>n>>d;
    for(int i=1;i<=n;i++) {
        cin>>a[i].pos;
        a[i].id=i;
    }
    sort(a+1,a+1+n,cmp);
    vector<int> ans;
    if(abs(a[1].pos-a[2].pos)>=d) ans.push_back(a[1].id);
    for(int i=2;i<n;i++) {
        if(abs(a[i].pos-a[i-1].pos)>=d&&abs(a[i].pos-a[i+1].pos)>=d) {
            ans.push_back(a[i].id);
        }
    }
    if(abs(a[n].pos-a[n-1].pos)>=d) ans.push_back(a[n].id);
    sort(ans.begin(),ans.end());
    cout<<ans.size()<<endl;
    for(int v:ans) cout<<v<<" ";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    //cin>>T;
    while (T--) {
        solve();
    }
    return 0;
}

```

## 			C - Range Search Query 		 	

### 题意简述

给定字符串 $S$ 和 $T$。处理 $Q$ 个查询。在每个查询中，给定 $L$ 和 $R$。判断由 $S$ 的第 $L$ 个字符到第 $R$ 个字符组成的子串是否包含 $T$ 作为子串。

### 题解

这道题 $T$ 的长度特别短，所以我们只需要简单预处理就行了，学了一招 `string` 的 `compare` 函数。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 4e5+100;
#define endl '\n'
int pos[MAXN];
void solve() {
    int q;
    string s,t;
    cin>>q;
    cin>>s;
    cin>>t;
    int n=s.size(),m=t.size();
    s=" "+s;
    pos[n+1]=-1;

    for(int i=n;i>=1;i--) {
        pos[i]=pos[i+1];
        if(i+m-1<=n && s.compare(i,m,t)==0) {
            pos[i]=i+m-1;
        }
    }
    //for(int i=1;i<=n;i++) cout<<"debug "<<pos[i]<<endl;
    while(q--) {
        int l,r;
        cin>>l>>r;
        if(pos[l]==-1) {
            cout<<"No"<<endl;
        }
        else if(r>=pos[l]) {
            cout<<"Yes"<<endl;
        }
        else {
            cout<<"No"<<endl;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    //cin>>T;
    while (T--) {
        solve();
    }
    return 0;
}

```

## 			D - Masking Tape 		 	

### 题意简述

有 $N$ 个方格排成一行，从左到右编号为方格 $1$ 到方格 $N$。颜色用小写英文字母表示。

最初，每个方格的颜色都是 `a`，且任何方格上都没有放置任何东西。

给定 $Q$ 个查询；按给定顺序处理它们。每个查询属于以下两种类型之一：

- $1\ X$：如果方格 $X$ 上没有放置瓷砖，则在其上放置一个瓷砖；如果其上已放置瓷砖，则将其移除。
- $2\ C$：将所有未放置瓷砖的方格的颜色改为 $C$。

在处理完所有查询后，求出每个方格的颜色（无论其上是否放置了瓷砖）。

### 题解

用时间戳的思想维护染色，每次查询直接 $O(1)$ ，轻松通过。这里要注意移除瓦片不会改变方格的颜色，所以不能认为所有没有瓦片的方格颜色都相同。

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
    int t=0;
    cin>>n>>q;
    vector<bool> vis(n+1,0);
    vector<int> lst(n+1,0);
    vector<char> a(n+1,'a');
    char c='a';
    while(q--) {
        int op;
        cin>>op;
        if(op==1) {
            int x;
            cin>>x;
            if(!vis[x]&&lst[x]<t) {
                a[x]=c;
            }
            vis[x]=!vis[x];
            lst[x]=t;
        }
        else {
            cin>>c;
            t++;
        }
    }
    for(int i=1;i<=n;i++) {
        if(!vis[i]&&lst[i]<t) {
            a[i]=c;
        }
        cout<<a[i];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    //cin>>T;
    while (T--) {
        solve();
    }
    return 0;
}

```

## 			E - Wheel Distance 		 	

### 题意简述

给定一个边加权无向图，包含 $N+1$ 个顶点，编号为 $1$ 到 $N+1$。
对于每个满足 $1\le i\le N$ 的整数 $i$，存在一条权重为 $A_i$ 的边连接顶点 $i$ 和顶点 $(i\bmod N)+1$。
此外，对于每个满足 $1\le i\le N$ 的整数 $i$，存在一条权重为 $B_i$ 的边连接顶点 $i$ 和顶点 $N+1$。不存在其他边。

处理 $Q$ 个查询。每个查询给定 $S$ 和 $T$；求从顶点 $S$ 到顶点 $T$ 的最短路径长度。

### 题解

很显然，任意给两个点 $u$ ，$v$，我要不然就是直接绕着这个环走过去，要不然就是我先走到 $n+1$ 这个点再走过去，取一下最小值就行了。我们可以直接用 `Dijkstra` 维护 $n+1$ 到所有点的最短路，然后维护一下前缀和，分别对应着两种走法，注意前缀和要考虑环的问题，并且题目给的是边权而不是点权。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'
#define int long long
vector<pair<int,int>> edge[MAXN];
int n,q,dis[MAXN];
priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> que;
bool vis[MAXN];
int sum[MAXN];
signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n>>q;
    for(int i=1;i<=n;i++) {
        int x;
        cin>>x;
        sum[i]=sum[i-1]+x;
        edge[i].push_back({(i%n)+1,x});
        edge[(i%n)+1].push_back({i,x});
    }
    for(int i=1;i<=n;i++) {
        int x;
        cin>>x;
        edge[i].push_back({n+1,x});
        edge[n+1].push_back({i,x});
    }
    int s=n+1;
    memset(dis,0x7f,sizeof(dis));
    dis[s]=0;
    que.push({0,s});
    while(!que.empty()) {
        int u=que.top().second;
        que.pop();
        if(vis[u]) continue;
        vis[u]=true;
        for(auto ed:edge[u]) {
            int v=ed.first;
            int w=ed.second;
            if(dis[v]>dis[u]+w) {
                dis[v]=dis[u]+w;
                que.push({dis[v],v});
            }
        }
    }
    while(q--) {
        int u,v;
        cin>>u>>v;
        if(v==n+1) {
            cout<<dis[u]<<endl;
        }
        else {
            int tmp=sum[v-1]-sum[u-1];
            cout<<min(min(tmp,sum[n]-tmp),dis[u]+dis[v])<<endl;
        }
    }
    return 0;
}

```
