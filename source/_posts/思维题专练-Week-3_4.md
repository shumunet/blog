---
title: "思维题专练 Week 3-4"
description: "整理一些思维与构造题，树木又进步了喵～"
cover: /img/covers/acg-003.jpg
date: 2026-11-01 22:30:00
categories:
  - 算法竞赛
tags:
  - 构造
  - 专项练习
math: true
---

## 前言

因为本人的构造能力实在是有点太唐了，所以我从 10 月 6 日开始打算刷一些思维题提升提升能力，这是第三周和第四周做的题。另外，本次涉及到了博客的更新：取消题意简述，转为直接贴题目链接。

## CF1374D Zero Remainder Array

### 题意简述

给你一个由 $n$ 个正整数组成的数组 $a$ 和一个正整数 $k$，你可以进行以下两种操作：

1. $x$ 自增。
2. 将 $a$ 中任意一个数字增加 $x$，然后 $x$ 自增。

特别地，操作 $2$ 对一个位置只能进行一次，$x$ 的初始值是 $0$。

数据范围：$1 \le n \le 2 \cdot 10^5; 1 \le k \le 10^9; 1 \le a_i \le 10^9$。

### 题解

手玩样例容易注意到我们可以 $O(n)$ 算出每个数需要加的数字，然后可以贪心去加当前差最小的，如果当前最小的差已经比 $x$ 小了则给它加上 $x$ 然后继续走。这里一开始想的是用堆模拟，体感应该是 $O(n \log n)$，实际上令所有的 $a_i$ 相等是可以给我卡退化的，于是喜提超时。考虑优化，注意到可以不模拟，直接加就行了，在预处理阶段就给 $k$ 加上，维护一个 map 记录差值出现次数就可以做到。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'
#define int long long 

void solve() {
    int n,k;
    cin>>n>>k;
    map<int,int> cnt;
    ll ans=0;
    for(int i=1;i<=n;i++) {
        int x;
        cin>>x;
        int d=(k-x%k)%k;
        if(d==0) continue;
        cnt[d]++;
        ans=max(ans,d+1LL*(cnt[d]-1)*k+1);
    }
    cout<<ans<<endl;
}
signed main() {
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

## P6599 「EZEC-2」异或

### 题意简述

有 $T$ 组询问，每次给定两个正整数 $n,l$，   

你需要构造一个长度为 $l$ 的正整数序列 $a$（编号从 $1$ 至 $l$），   

且满足 $\forall i\in[1,l]$，都有 $a_i\in[1,n]$。

最大化：

$$\sum_{i=1}^l\sum_{j=1}^{i-1}a_i\oplus a_j$$

为了避免答案过大，对于每组询问，只需要输出这个最大值对 $10^9+7$ 取模的结果。

数据范围：$1\le T\le 5\times10^5$，$1\le n\le 10^{12}$，$2\le l \le 10^5$。

### 题解

我们考虑用一个贪心：给定一个数接下来构造一个数和它异或得到的结果，那就是把这个数完全取反。这里因为是维护最大的异或和，那我们局部最大就一定能得到全局最大，所以可以直接上贪心。

怎么贪心呢？注意到我们直接把能取到的上界拿过来，那么它的最高位 1 一定是这个序列中所有出现的数中最高位的 1 的位数里面最大的，所以接下来出现的数都不会超过最大值。

有了这个思路，很快就写出了这个代码：

```c++
vector<ll> ans;
ans.push_back(n);
now=n;
for(int i=2;i<=l;i++) {
    ll tmp=0;
    for(int j=63;j>=0;j--) {
        if((tmp|((((now>>j)&1)^1)<<j))<=n) {
            tmp|=((((now>>j)&1)^1)<<j);
        }
    }
    now=tmp;
    ans.push_back(tmp);
}
```

这样构造得到了 $50pts$，有错误的同时超时了，于是分析一下，发现当 $n$ 的二进制位恰好全是 1 的时候我们就造出了非法的 0 了，这个很好解决，特判一下如果是的话取全 1 就没有这个问题了，但是常数确实太大了，考虑优化。

打个表，观察到序列一定是交替出现的，这是因为我们一直在取反一个数，那这道题就迎刃而解了。

令 $p$ 是不超过 $n$ 的最大二次幂。当 $n\ge2$ 时，直接让 $p$ 和 $p - 1$ 交替出现。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = unsigned long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    ll n,l;
    cin>>n>>l;
    if(n==1) {
        cout<<0<<endl;
        return;
    }
    ll p=1;
    while(p*2<=n) {
        p*=2;
    }
    ll res=(2*p-1)%MOD;
    res=res*(l/2)%MOD;
    res=res*((l+1)/2)%MOD;
    cout<<res<<endl;
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

## P12373 「LAOI-12」命运。

### 题意简述

多测，给定正整数 $n$，请你构造一个长度为 $n$ 的**排列**使得其所有区间极差之和为 $\sum\limits_{i=1}^{n-1}i^2$。

数据范围：$1\le T\le 10^3$，$2\le n,\sum n \le10^6$。

### 题解

考虑从小到大，从大到小交替取数。

考虑相邻值 $k$ 与 $k+1$ 之间的“值域分界”，一个区间极差为 $d$ 恰好跨过 $d$ 个这样的区间，这样就构造完了。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    int tmp1=1,tmp2=n;
    for(int i=1;i<=n;i++) {
        if(i%2==1) cout<<tmp1++<<" ";
        else cout<<tmp2--<<" ";
    }
    cout<<endl;
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

## CF1909C Heavy Intervals

### 题意简述

有 $n$ 个区间 $[l_1, r_1], [l_2, r_2], \dots, [l_n, r_n]$，其中对于每个 $i$，都有 $l_i < r_i$，并且所有区间的端点都是互不相同的。

第 $i$ 个区间每单位长度的权值为 $c_i$。因此，第 $i$ 个区间的总权值为 $c_i \cdot (r_i - l_i)$。

你不喜欢大的权值，所以你希望使所有区间的权值和尽可能小。你可以进行以下三种操作：

- 任意重排数组 $l$ 中的元素；
- 任意重排数组 $r$ 中的元素；
- 任意重排数组 $c$ 中的元素。

但是，所有操作完成后，区间仍需合法（即对于每个 $i$，都要满足 $l_i < r_i$）。

在进行操作后，区间权值和的最小可能值是多少？

数据范围：$1\le t\le 10^4,\ 1\le n\le 10^5,\ \sum n\le 10^5,\ 1\le l_i<r_i\le 2\cdot10^5,\ 1\le c_i\le 10^7$，所有端点互不相同。

### 题解

非常容易想到我们应该用尽可能小的 $c$ 去匹配尽可能元素多的区间。显然 $c$ 是可以直接排序的，结合数据范围可以确定本题的时间复杂度就是 $O(n \log n)$。接下来发现 $c$ 排序后还要维护当前元素最多的区间，这是个动态问题，可以使用堆来维护，这样才能让单次变成 $O(\log n)$。想到这里，就是怎么放到堆里面了，显然我们可以给 $r$ 排序，然后每个 $r$ 都找到离它最近的 $l$，这显然可以二分，随后放到堆里面处理就行了（事后发现其实根本不用堆，直接排序也是一样的）。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    ll n;
    cin>>n;
    vector<ll> r(n),c(n);
    set<ll> l;
    priority_queue<ll> que; 
    for(int i=0;i<n;i++) {
        ll x;
        cin>>x;
        l.insert(x);
    }
    for(int i=0;i<n;i++) cin>>r[i];
    for(int i=0;i<n;i++) cin>>c[i];
    sort(c.begin(),c.end());
    sort(r.begin(),r.end());
    for(int i=0;i<n;i++) {
        auto it=l.lower_bound(r[i]);
        it--;
        que.push(r[i]-*it);
        l.erase(it);
    }
    ll ans=0;
    for(int i=0;i<n;i++) {
        ans+=que.top()*c[i];
        que.pop();
    }
    cout<<ans<<endl;
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

## B3683 [语言月赛202211] String Problem

### 题意简述

给出两个长度为 $n$ 的字符串 $s$ 和 $t$，进行 $q$ 次修改，每次修改都是将 $s$ 或 $t$ 中的指定位置修改为指定字符，每次修改后直接输出 $s$ 是否等于 $t$。

数据范围：字符串长度不超过 $10^6$，$q \le 10^6$。

### 题解

首先考虑暴力，就是直接暴力修改再判断呗，但是每次判断是 $O(n)$，这样哪怕是超级计算机也会喜提超时。考虑优化，我们可以存储不相等的位置，这样就做完了。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n,q;
    cin>>n>>q;
    string s,t;
    cin>>s>>t;
    int cnt=0;
    for(int i=0;i<n;i++) if(s[i]!=t[i]) cnt++;
    if(!cnt) cout<<"Yes"<<endl;
    else cout<<"No"<<endl;
    while(q--) {
        int o,p;
        char c;
        cin>>o>>p>>c;
        if(t[p-1]!=s[p-1]) cnt--;
        if(o==1) s[p-1]=c;
        else t[p-1]=c;
        if(t[p-1]!=s[p-1]) cnt++;
        if(!cnt) cout<<"Yes"<<endl;
        else cout<<"No"<<endl;
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

## [Yesterday Once More (Easy Version)](https://qoj.ac/problem/17353)

我也不知道咋注意到的，就是先考虑绕过去，然后发现有一些特殊情况，讨论讨论就能出来。

显然，我这道题看了题解 T_T

```	c++
#include<bits/stdc++.h>
using namespace std;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    string s;
    for(int i=1;i<=n;i++) s+="D";
    s+="RDDL";
    for(int i=1;i<=n;i++) s+="D";
    for(int i=1;i<=n;i++) s+="RDDLL";
    for(int i=1;i<=n;i++) s+="URRD";
    for(int i=1;i<=n;i++) s+='L';
    s+="DL";
    for(int i=1;i<=n;i++) s+='D';
    cout<<s.size()<<endl;
    cout<<s;
}

int main() {
    int T=1;
    //cin>>T;
    while(T--) {
        solve();
    }
}
```

## [Triple Removal](https://codeforces.com/problemset/problem/2152/C)

一次性可以消除三个相同字符，那显然查询区间里面的 1 的数目不是 3 的倍数或者 0 的数目不是 3 的倍数就不合法，否则就合法。

上面的过程用前缀和统计是很容易的。下面讨论有解情况。

因为一次消除 3 个，所以总操作数 $T=\frac{cnt_0}{3}+\frac{cnt_1}{3}$。

现在我们考虑怎么最小化代价。注意到如果存在两个数字是连续的，那么就可以用 1 的代价消除远端的数。想到这里，模拟了一下样例，发现只要存在两个数字是连续的，我们就可以消掉类似于 `010` 或者 `101` 中间的位置得到新的连续的数字（当然有可能原本就有新的连续数字）。这样的话我们每次消除代价都是 1，答案显然就是 $T$。

当然，还有可能是纯粹的 01 交替，这种时候显然需要先删 1 次才能得到数字连续，第一次删除代价多了 1，答案是 $T+1$。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n,q;
    cin>>n>>q;
    vector<int> a(n+1,0),cnt0(n+1,0),cnt1(n+1,0),same(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
        cnt0[i]=cnt0[i-1],cnt1[i]=cnt1[i-1];
        if(a[i]==0) cnt0[i]++;
        else cnt1[i]++;
        if(i>=2) {
            same[i]=same[i-1]+(a[i]==a[i-1]);
        }
    }
    while(q--) {
        int l,r;
        cin>>l>>r;
        int zero=cnt0[r]-cnt0[l-1];
        int one=cnt1[r]-cnt1[l-1];
        if(zero%3!=0||one%3!=0) {
            cout<<-1<<endl;
            continue;
        }
        int len=r-l+1;
        int ans=len/3;
        if(same[r]-same[l]==0) ans++;
        cout<<ans<<endl;
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

## [Voting](https://codeforces.com/problemset/problem/749/C)

显然，最优策略就是禁言下一个发言的敌方。但是这个东西是很难维护的，我们思考它的本质。

发言完之后等所有人发言完才能继续发言，所以这个结构很像是一个队列，那么我们就可以使用队列来模拟。

问题在于，我怎么维护每个人应该禁言的人呢？这个用队列显然无法实现。

于是，我们可以使用两个变量存储当前还剩下的禁言次数，遇到一个人先看它敌对阵营有没有禁言，如果有的话它就被禁言了，否则它可以禁言一个人。

这样模拟的话这道题就做完了。实现有个细节就是要维护可发言的，不然最后如果剩下都是一个阵营的就死循环了。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    queue<char> que;
    int sD=0,sR=0;
    for(int i=1;i<=n;i++) {
        char x;
        cin>>x;
        que.push(x);
        if(x=='D') sD++;
        else sR++;
    }
    int cntD=0,cntR=0;
    while(!que.empty()&&sR!=0&&sD!=0) {
        char now=que.front();
        que.pop();
        if(now=='D') {
            if(cntR>0) {
                cntR--;
                sD--;
            }
            else {
                que.push(now);
                cntD++;
            }
        }
        else {
            if(cntD>0) {
                cntD--;
                sR--;
            }
            else {
                que.push(now);
                cntR++;
            }
        }
    }
    if(!sR) cout<<'D';
    else cout<<'R';
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

## [**Escape Route**](https://atcoder.jp/contests/adt_all_20260916_2/tasks/abc405_d)

魔改一下 `BFS`，在扩展的时候标上路线，因为首次搜到的路径就是最短路径。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e3+100;
#define endl '\n'

int n,m;
char mp[MAXN][MAXN];
bool vis[MAXN][MAXN];
queue<pair<int,int>> que;

bool check(int x,int y) {
    if(x>n||x<1||y>m||y<1||vis[x][y]||mp[x][y]=='#') return false;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n>>m;
    for(int i=1;i<=n;i++) {
        for(int j=1;j<=m;j++) {
            cin>>mp[i][j];
            if(mp[i][j]=='E') {
                que.push({i,j});
                vis[i][j]=true;
            }
        }
    }
    while(!que.empty()) {
        auto [x,y]=que.front();
        que.pop();
        if(check(x+1,y)) {
            mp[x+1][y]='^';
            vis[x+1][y]=true;
            que.push({x+1,y});
        }
        if(check(x-1,y)) {
            mp[x-1][y]='v';
            vis[x-1][y]=true;
            que.push({x-1,y});
        }
        if(check(x,y+1)) {
            mp[x][y+1]='<';
            vis[x][y+1]=true;
            que.push({x,y+1});
        }
        if(check(x,y-1)) {
            mp[x][y-1]='>';
            vis[x][y-1]=true;
            que.push({x,y-1});
        }
    }
    for(int i=1;i<=n;i++) {
        for(int j=1;j<=m;j++) {
            cout<<mp[i][j];
        }
        cout<<endl;
    }
    return 0;
}
```

## [Reorder Cards](https://atcoder.jp/contests/adt_all_20260723_2/tasks/abc213_c)

一行只要含有编号卡片，就不会被删除；删除空行不会改变其他有编号卡片的相对顺序。因此，卡片最终的行号就是它上方有多少个**不同的非空行**，再加 $1$。列方向同理。而在 C++ 中有很多方便的 STL 能达到我们想要的目的，这里使用 `unique` 和 `lower_bound`。

```c++
#include<bits/stdc++.h>
using namespace std;
#define endl '\n'

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h,w,n;
    cin>>h>>w>>n;
    vector<int> a(n),b(n),rows,cols;
    for(int i=0;i<n;i++) {
        cin>>a[i]>>b[i];
        rows.push_back(a[i]);
        cols.push_back(b[i]);
    }
    sort(rows.begin(),rows.end());
    rows.erase(unique(rows.begin(),rows.end()),rows.end());
    sort(cols.begin(),cols.end());
    cols.erase(unique(cols.begin(),cols.end()),cols.end());
    for(int i=0;i<n;i++) {
        int r=lower_bound(rows.begin(),rows.end(),a[i])-rows.begin()+1;
        int c=lower_bound(cols.begin(),cols.end(),b[i])-cols.begin()+1;
        cout<<r<<" "<<c<<endl;
    }
    return 0;
}
```

## [Edge Addeleting](https://codeforces.com/contest/2277/problem/C)

一个很好的 Div.2C。首先我们手玩样例，很容易观察到如果 $1、v、n$ 不在同一个子树上的话这条边加上来不会对答案产生任何贡献，如果在的话最优解就是删除掉 $1$ 到 $v$ 原本的第一步，这样整条链都会断掉，最短路变成从 $1$ 走一步到 $v$ 再从 $v$ 走到 $n$，因为是树的结构，所以这一定是正确的。那么算法的瓶颈就在快速处理 $v$ 走到 $n$ 的最短路了，这里其实可以直接以 $n$ 为起点计算单源最短路，但是因为所有边权都是 $1$ 所以使用 `BFS` 搜一边就结束了。

哦不不不，其实没有结束，我们怎么判断在不在一个子树呢？一开始想的并查集，后面发现搜索过程中维护就结束了。

``` c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n,m;
    cin>>n>>m;
    vector<vector<int>> edge(n+1);
    vector<int> d(n+1,0);
    vector<bool> vis(n+1,0),in_sub(n+1,0);
    for(int i=1;i<n;i++) {
        int u,v;
        cin>>u>>v;
        edge[u].push_back(v);
        edge[v].push_back(u);
    }
    queue<int> que;
    que.push(n);
    vis[n]=true;
    in_sub[1]=true;
    while(!que.empty()) {
        int u=que.front();
        que.pop();
        for(int v:edge[u]) {
            if(vis[v]) continue;
            d[v]=d[u]+1;
            vis[v]=true;
            if(in_sub[u]) in_sub[v]=true;
            que.push(v);
        }
    }
    int ans=d[1];
    for(int i=1;i<=m;i++) {
        int v;
        cin>>v;
        if(!in_sub[v]) ans=max(ans,d[v]+1);
    }
    cout<<ans<<endl;
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

## [Friends](https://codeforces.com/problemset/problem/94/B)

诈骗题，这有 1300 ？！

注意到只有 $5$ 个人， 考虑图论建模，直接暴力枚举解决。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

bool flag[6][6];
int m;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>m;
    for(int i=1;i<=m;i++) {
        int u,v;
        cin>>u>>v;
        flag[u][v]=true;
        flag[v][u]=true;
    }
    bool ok=false;
    for(int i=1;i<=5;i++) {
        for(int j=1;j<=5;j++) {
            for(int k=1;k<=5;k++) {
                if(i==j||j==k||i==k) continue;
                if(flag[i][j]&&flag[j][k]&&flag[i][k]) ok=true;
                if(!flag[i][j]&&!flag[j][k]&&!flag[i][k]) ok=true;
            }
        }
    }
    if(ok) cout<<"WIN";
    else cout<<"FAIL";
    return 0;
}
```

## [Subsequence Hate](https://codeforces.com/problemset/problem/1363/B)

因为题目要求的是子序列而不是子串，所以只有以下四种结构的字符串是符合要求的：

- 全是 0
- 全是 1
- 前面全是 0 后面全是 1
- 前面全是 1 后面全是 0

否则我通过删除一定可以得到 `010` 或者 `101` 的。接下来考虑快速求出操作，因为字符串长度的值域不是特别大，我们可以考虑枚举分割点，然后处理操作数，操作数的维护可以使用维护 `前缀 0 的数目` 和 `前缀 1 的数目` 来解决。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    string s;
    cin>>s;
    int n=s.size();
    s=" "+s;
    vector<int> cnt0(n+1,0),cnt1(n+1,0);
    for(int i=1;i<=n;i++) {
        cnt0[i]=cnt0[i-1];
        cnt1[i]=cnt1[i-1];
        if(s[i]=='0') cnt0[i]++;
        else cnt1[i]++;
    }
    int ans=0x7f7f7f7f;
    for(int i=1;i<=n;i++) {
        ans=min(ans,(cnt0[i-1]+cnt1[n]-cnt1[i-1]));
        ans=min(ans,cnt1[i-1]+cnt0[n]-cnt0[i-1]);
    }
    cout<<ans<<endl;
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

## [Garland](https://codeforces.com/contest/408/problem/B)

读题难度非常大，但是实际上很简单。只需要维护需要的和我有的然后取最值就行了。这里用 `map` 快速实现哈希表。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    string s,t;
    cin>>s>>t;
    map<char,int> cnt;
    map<char,int> need;
    int n=s.size(),m=t.size();
    for(int i=0;i<n;i++) cnt[s[i]]++;
    for(int i=0;i<m;i++) need[t[i]]++;
    for(int i='a';i<='z';i++) {
        if(need[i]&&!cnt[i]) {
            cout<<-1;
            return;
        }
    }
    int ans=0;
    for(int i='a';i<='z';i++) {
        ans+=min(need[i],cnt[i]);
    }
    cout<<ans;
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

## [Remove Two Letters](https://codeforces.com/contest/1800/problem/D)

首先暴力枚举肯定是会超时的，那我们正难则反，我们考虑用总方案减去相同方案。

我们假设不考虑相同字符串的问题，从长度为 $n$ 的字符串中选择 $2$ 个连续位置删除显然会得到 $n-1$ 种结果，那么我们考虑什么样的字符串会相同。

通过玩弄样例，容易发现存在 `aba` 这样的结构会导致出现相同的字符串，其实很好理解，对于字符串 `T+"aba"+S`，删除 `ab` 会得到 `T+"a"+S` ，删除 `ba` 也会得到 `T+"a"+S`，于是直接统计所有的 `aba` 型子串数目，再用 $n-1$ 减去它就是答案。

值得一提的是， `aaa` 型其实是 `aba` 型的一种特殊情况。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    string s;
    cin>>s;
    int cnt=0;
    for(int i=0;i<n-2;i++) {
        if(s[i]==s[i+2]) cnt++;
    }
    int ans=n-1;
    ans-=cnt;
    cout<<ans<<endl;
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

## [Basil's Garden](https://codeforces.com/contest/1987/problem/C)

依旧正难则反，考虑最后一个数字变成 $0$ 显然花费是最后一个数字，前面的数字我们对 $a_i$ 进行分类讨论：

- 如果 $a_i \le a_{i+1}$，则 $a_{i+1}$ 变成 $0$ 的时候 $a_i=1$，再进行 $1$ 的花费即可归零。
- 否则，需要花费 $i$ 的时间，因为是同时操作所以与其他的是不影响的。

当然，最后一个数 $a_n$ 是不受上面的约束的，它每次都会下降。于是我们可以倒着推，进行分类讨论取最值。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    vector<int> a(n+1,0);
    for(int i=1;i<=n;i++) cin>>a[i];
    for(int i=n-1;i>=1;i--) a[n]=max(a[n]+1,a[i]);
    cout<<a[n]<<endl;
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

## [Delete Two Elements](https://codeforces.com/contest/1598/problem/C)

设原本数组的平均值是 $k$，若想让删除两个数后数组的平均值还是 $k$，就需要被删除的两个数的平均值是 $k$，朴素的做法是 $O(n^2)$ 枚举一遍，但是这显然是 TLE 的，为了不 TLE 我们可以考虑遍历一遍数组来维护答案。维护一个 `cnt` ，用于统计前缀中数字出现的次数，如果 $a_i$ 和之前某个出现过的数字的平均值是 $k$ 那么根据加法原理则会对答案产生这个数出现次数的贡献。问题变成怎么快速找到这个数。这个数字的结果显然就是 $2k-a_i$，但是因为浮点数会丢失精度，所以我们可以去二分比它大的最小值和比它小的最大值，看看是不是和 $a_i$ 的平均数正好是 $k$，就解决了这个问题。

> 警告：浮点数判断是否相同要用差的绝对值小于等于 eps 来判定，不可直接判断是否相等！

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define int long long
#define endl '\n'

void solve() {
    int n;
    long double k=0;
    cin>>n;
    vector<int> a(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
        k+=a[i];
    }
    k/=n;
    map<int,int> cnt;
    set<int> st;
    int ans=0;
    for(int i=1;i<=n;i++) {
        auto it=st.lower_bound(2*k-a[i]);
        if(it!=st.end()) {
            if(abs(((long double)*it+a[i])/2-k)<=1e-6) ans+=cnt[*it];
        }
        if(it!=st.begin()) {
            it--;
            if(abs(((long double)*it+a[i])/2-k)<=1e-6) ans+=cnt[*it];
        }
        st.insert(a[i]);
        cnt[a[i]]++;
    }
    cout<<ans<<endl;
}

signed main() {
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

