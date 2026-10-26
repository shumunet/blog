---
title: "状压 DP 学习笔记"
description: "介绍状态压缩的思想，同时练习一些经典题目。"
cover: /img/covers/acg-007.jpg
date: 2026-10-26 16:30:00
categories:
  - 算法竞赛
tags:
  - 学习笔记
  - 动态规划
math: true
---

## 前言

> 更新：更新了简介并更新了一道题。

考虑一个动态规划中遇到的问题：给你 $n$ 个数，有依赖性，比如说我用了第 1 个数就不能用第 3 个数。这时我们显然可以用一个布尔数组表示某个数字能不能继续使用，但是这样的话就会导致可能性非常多，于是我们考虑用整的位信息来表示路径，这样就能节省空间的同时方便我们表达状态。

> 状压DP：设计一个可变参数 status，利用 status 的位信息，来表示某个样本是否可以使用，然后利用这个信息去进行尝试。显然，如果有 $k$ 个样本，表示这些样本数量就是 $2^k$（乘法原理）。

注意到样本增加一个，状态数量是指数级增长，所以状压DP对应的数据量是不大的。

如果样本数量普通的状压DP无法解决，可以考虑**双向广搜**。

## [P2622 关灯问题 II](https://www.luogu.com.cn/problem/P2622)

显然，我们可以用 1 表示开灯，0 表示关灯，存放在一个 `int` 变量中。

一开始全部都是开着的，那就是全 1，可以使用左移减 1 来快速得到。

目标是全 0，也就是 0。

因为题目要的是最短路径，我们考虑 `bfs` ，这道题就做完了。

其中有一些位运算技巧，这篇博客就先不讲了，以后会专门发一篇博客来讲。

```c++
#include<bits/stdc++.h>
using namespace std;
#define endl '\n'

int n,m,a[110][20],vis[(1<<10)+5],dp[(1<<10)+5];
queue<int>que;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    memset(dp,0x7f,sizeof(dp));
    cin>>n>>m;
    for(int i=1;i<=m;i++) {
        for(int j=1;j<=n;j++) {
            cin>>a[i][j];
        }
    }
    int x=(1<<n)-1;
    que.push(x);
    vis[x]=1;
    dp[x]=0;
    while(!que.empty()) {
        int tmp=que.front();
        que.pop();
        if(tmp==0) {
            cout<<dp[tmp];
            return 0;
        }
        for(int i=1;i<=m;i++) {
            int xx=tmp;
            for(int j=1;j<=n;j++) {
                if(a[i][j]==1) {
                    xx&=((1<<n)-1)-(1<<(j-1));
                }
                else if(a[i][j]==-1) {
                    xx|=(1<<(j-1));
                }
            }
            if(!vis[xx]) {
                vis[xx]=1;
                que.push(xx);
            }
            dp[xx]=min(dp[xx],dp[tmp]+1);
        }
    }
    cout<<-1;
    return 0;
}
```

## [P1123 取数游戏](https://www.luogu.com.cn/problem/P1123)

这道题其实正常 `DFS` 也能搜过去，这里为了方便学习我们使用 `状压DP`。

设 `dp[i][s]` 表示处理完前 $i$ 行，且第 $i$ 行选取状态为 $s$ 时的最大和。

把一行的 $M$ 个位置用二进制表示，$s$ 的第 $j$ 位为 $1$ 就表示选了这一格。相邻的格子不能同取，所以同一行中不能有相邻的 $1$，即：

```c++
(s & (s << 1)) == 0;
```

再考虑相邻两行：若上一行选了第 `j` 列，那么当前行的第 $j-1$、$j$、$j+1$ 列都不能选。

```c++
(s & p) == 0;
(s & (p << 1)) == 0;
(s & (p >> 1)) == 0;
```

令 `sum[i][s]` 为第 `i` 行按状态 `s` 选中数字的和，则转移为：

```c++
dp[i][s] = max(dp[i - 1][p] + sum[i][s]);
```

初始化显然就是把 `dp[0][0]` 赋值为 0。

```c++
#include<bits/stdc++.h>
using namespace std;
#define endl '\n'

int n,m,a[10][10],st[1<<6],cnt;
long long dp[7][1<<6];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin>>T;
    while(T--) {
        cin>>n>>m;
        for(int i=1;i<=n;i++) {
            for(int j=1;j<=m;j++) {
                cin>>a[i][j];
            }
        }

        cnt=0;
        for(int s=0;s<(1<<m);s++) {
            if((s&(s<<1))==0) {
                st[++cnt]=s;
            }
        }

        memset(dp,0,sizeof(dp));
        for(int i=1;i<=n;i++) {
            for(int x=1;x<=cnt;x++) {
                int s=st[x];
                long long sum=0;
                for(int j=1;j<=m;j++) {
                    if(s&(1<<(j-1))) {
                        sum+=a[i][j];
                    }
                }

                for(int y=1;y<=cnt;y++) {
                    int p=st[y];
                    if((s&p)==0&&(s&(p<<1))==0&&(s&(p>>1))==0) {
                        dp[i][s]=max(dp[i][s],dp[i-1][p]+sum);
                    }
                }
            }
        }

        long long ans=0;
        for(int x=1;x<=cnt;x++) {
            ans=max(ans,dp[n][st[x]]);
        }
        cout<<ans<<endl;
    }
    return 0;
}
```

## [P1896 [SCOI2005] 互不侵犯](https://www.luogu.com.cn/problem/P1896)

这道题难度就稍微大一些了，但是思想还是状态压缩。

（这道题非常重要来着，所以如果看到了记得提醒作者去复习 /doge）

设 $dp_{i,j,l}$ 表示前 $i$ 行，第 $i$ 的状态是 $j$，已经放置了 $l$ 个国王的方案数。

对于一个状态 $j$，我们用 $sit(j)$ 表示国王的放置情况，某个二进制位为 1 表示这个位置放了国王，否则就是没放。用 $sta(j)$ 表示放置国王数目，显然就是 $j$ 二进制位中 $1$ 的数目。

设上一行状态为 $x$，当前行状态为 $j$，则：

$$dp_{i,j,l}=\sum dp_{i-1,x,l-sta(j)}$$

其中要求状态合法。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define endl '\n'

ll n,k,dp[15][(1<<10)][15],sta[2100],sit[2100],cnt;

void dfs(int x,int num,int cur) {
    //x 表示摆法，num 表示国王数目，cur 表示正在处理的列
    //枚举一行中所有不互相攻击的国王摆法，并记录每种摆法的状态和国王数量
    if(cur>=n) {
        sit[++cnt]=x;
        sta[cnt]=num;
        return;
    }
    dfs(x,num,cur+1); //cur位不放置国王
    dfs((x+(1<<cur)),num+1,cur+2); //cur位放国王
}

bool check(int j, int x) {
    //当前状态是否合法
    if(sit[j]&sit[x]) return false;
    if((sit[j]<<1)&sit[x]) return false;
    if(sit[j]&(sit[x]<<1)) return false;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n>>k;
    dfs(0,0,0);
    for(int j=1;j<=cnt;j++) dp[1][j][sta[j]]=1;
    for(int i=2;i<=n;i++) {
        for(int j=1;j<=cnt;j++) {
            for(int x=1;x<=cnt;x++) {
                if(!check(j,x)) continue;
                for(int l=sta[j];l<=k;l++) {
                    dp[i][j][l]+=dp[i-1][x][l-sta[j]];
                }
            }
        }
    }
    ll ans=0;
    for(int j=1;j<=cnt;j++) {
        ans+=dp[n][j][k];
    }
    cout<<ans;
    return 0;
}
```

## [P1171 售货员的难题](https://www.luogu.com.cn/problem/P1171)

这是一道 `TSP 问题`，是状态压缩动态规划的经典问题。

设 $dp_{mask,j}$ 表示从起点到 $j$ 号点且到达时状态为 $mask$ 的最短路，同样的 1 表示该村庄访问过，0 表示没有。

由于每个村庄恰好经过一次，所以 $mask$ 中含有 $i$ 并且没有 $j$ 就能从 $i$  走到 $j$，也就是：

```c++
dp[mask | (1 << j)][j] =
    min(dp[mask | (1 << j)][j], dp[mask][i] + s[i][j])
```

注意距离是**单向的**，因此转移使用 `s[i][j]`，不能假设它等于 `s[j][i]`。

所有村庄都访问后，还需要回到起点，再走一次回起点边就行了。

至于初始化，一开始是 1 号点，最短路显然是 0 ，也就是 $dp_{1,1} = 0$。

$dp$ 数组的更新可以用类似于 `floyd` 的思路来做，也就是枚举中间点。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define endl '\n'

const ll MAXN = 25;
const ll MAXS = 1<<21;
const ll INF = 1e18;

ll n,g[MAXN][MAXN],dp[MAXS][MAXN];

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n;
    for(int i=1;i<=n;i++) {
        for(int j=1;j<=n;j++) {
            cin>>g[i][j];
        }
    }
    // 访问集合用 0-based 位：村庄 i 对应第 i-1 位
    // 所以 mask=1 表示只访问了 1 号村庄
    fill(&dp[0][0], &dp[0][0] + MAXS * MAXN, INF);
    dp[1][1]=0;
    int full=(1<<n)-1;
    for(int mask=1;mask<=full;mask++) {
        if((mask&1)==0) continue; //必须包含起点
        for(int u=1;u<=n;u++) {
            if(dp[mask][u]==INF) continue;
            for(int v=2;v<=n;v++) {
                int bit=1<<(v-1);
                if(mask&bit) continue; //v 已经走过了（因为mask中它的位是 1）
                int nxt_mask=mask|bit; //访问 v
                dp[nxt_mask][v]=min(dp[nxt_mask][v],dp[mask][u]+g[u][v]);
            }
        }
    }
    ll ans=INF;
    for(int u=2;u<=n;u++) {
        ans=min(ans,dp[full][u]+g[u][1]);
    }
    cout<<ans;
    return 0;
}
```

## 总结

状态压缩动态规划主要分为以下三类：

- 旅行商类
- 集合类
- 棋盘类

本文已经涉及了这三类状态压缩动态规划问题。再深一步就是 `插头 DP` 和 `双向搜索` 等复杂技巧了，以后估计也会学学吧喵～
