---
title: "思维题专练 Week 5-6"
description: "整理一些思维与构造题，树木又进步了喵～"
cover: /img/covers/acg-014.jpg
date: 2026-11-15 22:17:00
categories:
  - 算法竞赛
tags:
  - 专项练习
  - 构造
math: true
---

## 前言

以后的话应该是改成一些需要观察 trick 的题目来进一步强化思维能力（？），我也不知豆啊。

## [Equalize by Divide](https://codeforces.com/contest/1799/problem/B)

看了看样例最后得到的基本都是全 2 序列，猜测 2 是解开这道题的关键因素。

玩了一些数字，大胆猜想一直除以 2 向上取整一定会得到 2，发现这个结论是正确的。

那么我们只需要先弄出来一个 2，然后接下来每个数字都一直除以 2 向上取整，最后弄出全 2 就行了。

因为我们一直除以 2，操作次数显然是对数级别，结合 $a_i<10^9$，每个数字的消耗一定是不到 30 的。

但是一定可以弄出来 2 吗？实际上并不行！！！！！

好了上面的做法其实是错误的，反例就是反复除得到 1 导致死循环。正解是啥呢？是一直让最大值和最小值操作。

```c++
#include<bits/stdc++.h>
using namespace std;
#define endl '\n'
const int MAXN = 2e5+100;
#define int long long

int a[MAXN];

void solve() {
    int n;
    cin>>n;
    if(n==1) {
        cin>>n;
        cout<<0<<endl;
        return;
    }
    for(int i=1;i<=n;i++) cin>>a[i];
    bool flag=true;
    for(int i=2;i<=n;i++) {
        if(a[i]!=a[i-1]) flag=false;
    }
    if(flag) {
        cout<<0<<endl;
        return;
    }
    for(int i=1;i<=n;i++) {
        if(a[i]==1) {
            cout<<-1<<endl;
            return;
        }
    }
    vector<pair<int,int>> ans;
    while(*min_element(a+1,a+1+n)!=*max_element(a+1,a+1+n)) {
        int pos=min_element(a+1,a+n+1)-a;
        int x=a[pos];
        for(int i=1;i<=n;i++) {
            if(i==pos||a[i]==x) continue;
            a[i]=(a[i]-1)/x+1;
            ans.push_back({i,pos});
        }
    }
    cout<<ans.size()<<endl;
    for(pair<int,int> v:ans) {
        cout<<v.first<<" "<<v.second<<endl;
    }
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

## [Sort](https://codeforces.com/contest/1996/problem/C)

观后感：莫队可以力大砖飞掉（x）

但是这么优美的一道题怎么能上这么暴力的结构呢，我们就想想到底在干嘛。

注意到要想排序后完全一样，显然所有字母的出现次数都相同是一个充分必要条件，于是直接维护前缀出现次数就解决了，用类似于前缀和的思想来做。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define endl '\n'

int id(char x) {
    return x-'a';
}

void solve() {
    int n,q;
    cin>>n>>q;
    string a,b;
    cin>>a>>b;
    a=" "+a;
    b=" "+b;
    vector<vector<int>> cnta(n+1,vector<int>(26)),cntb(n+1,vector<int>(26));
    for(int i=1;i<=n;i++) {
        for(int c='a';c<='z';c++) {
            cnta[i][id(c)]=cnta[i-1][id(c)],cntb[i][id(c)]=cntb[i-1][id(c)];
        }
        cnta[i][id(a[i])]++,cntb[i][id(b[i])]++;
    }
    while(q--) {
        int l,r;
        cin>>l>>r;
        int ans=0;
        for(int c=0;c<=25;c++) {
            ans+=abs((cnta[r][c]-cnta[l-1][c])-(cntb[r][c]-cntb[l-1][c]));
        }
        ans/=2;
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

## [A Balanced Problemset?](https://codeforces.com/contest/1925/problem/B)

整体还是很简单的，只需要找出 $x$ 的所有约数，然后用 $x$ 除以每个约数，看看这个值是不是大于等于 $n$，然后好像就做完了啊（

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define endl '\n'

void solve() {
    ll x,n,ans=0;
    cin>>x>>n;
    for(ll i=1;i*i<=x;i++) {
        if(x%i==0) {
            int k=x/i;
            if(k>=n) ans=max(ans,i);
            if(i!=x/i) {
                k=i;
                if(k>=n) ans=max(ans,x/i);
            }
        }
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

## [Math and Physics](https://codeforces.com/contest/2278/problem/C)

容易注意到当且仅当全是 $1$ 的时候没有办法合并为一个，否则一定可以分裂再传递下去。

然后根据样例注意到答案就是前缀和减去 $1$，交了一发 $WA$ 了，唐完了。

思考为什么都是 1，发现是因为中间有一些还会亏贡献，于是进行简单分类讨论，具体如代码所示。

实际上，这样分类讨论还是有点糖糖的，注意到可以直接维护 1 的数目，但是懒得写了。

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
    int n;
    cin>>n;
    vector<int> a(n+1,0);
    bool is_all_one=true;
    for(int i=1;i<=n;i++) {
        cin>>a[i];
        if(a[i]!=1) is_all_one=false;
    }
    if(is_all_one) {
        cout<<-1<<endl;
        return;
    }
    is_all_one=true;
    int ans=0;
    for(int i=1;i<=n;i++) ans+=a[i];
    for(int i=2;i<n;i++) if(a[i]!=1) is_all_one=false;
    if(is_all_one) {
        cout<<ans-n+1<<endl;
    }
    else {
        cout<<ans-1<<endl;
    }
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

## [Max Tree](https://codeforces.com/problemset/problem/2143/C)

利用差分约束的思想，我们可以把这道题用图论建模。

如果一条边的 $x>y$，那么我们要想让它取到更大的贡献 $x$ 就得要求 $p_u>p_v$，所以需要让 $v$ 排在 $u$ 的前面，可以建边 $v->u$；

否则的话，就需要 $u$ 在 $v$ 前面，可以建边 $u->v$。

然后直接跑拓扑排序，再把顶点转成排名，就做完了。

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
    vector<int> in_deg(n+1,0);
    vector<vector<int>> edge(n+1);
    for(int i=1;i<n;i++) {
        int u,v,x,y;
        cin>>u>>v>>x>>y;
        if(x>y) {
            edge[v].push_back(u);
            in_deg[u]++;
        }
        else {
            edge[u].push_back(v);
            in_deg[v]++;
        }
    }
    queue<int> que;
    for(int i=1;i<=n;i++) {
        if(in_deg[i]==0) que.push(i);
    }
    vector<int> p(n+1);
    int rank=1;
    while(!que.empty()) {
        int u=que.front();
        que.pop();
        p[u]=rank++;
        for(int v:edge[u]) {
            in_deg[v]--;
            if(in_deg[v]==0) {
                que.push(v);
            }
        }
    }
    for(int i=1;i<=n;i++) cout<<p[i]<<" ";
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

> 建图原理：拓扑排序规定对每条有向边 $a->b$ 都先取出 $a$ 再取出 $b$，所以可以这样建边代表谁在谁的前面。

## [[HNOI2015] 菜肴制作](https://www.luogu.com.cn/problem/P3243)

看到这种约束什么在什么之前的要求，就会想到拓扑排序，但是同时又要求了必须让小的数字尽可能先出现，那我们直接把拓扑排序的队列改成小根堆就结束了。但是这个贪心是错的，例如 $n=3,3\rightarrow1$，这时候我们这样贪心会输出 `2 3 1`。因为拓扑排序是让入度为 0 的先出现，这样就错了。怎么办呢？我们发现题目的两个要求都是要求谁先在前面出现，这容易左脑搏击右脑，那么我们可以逆向思维，倒着放答案。怎么实现呢？其实只需要倒着建图然后用大根堆就好了。

```c++
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
    vector<int> edge[MAXN];
    vector<int> in_deg(n+1,0);
    priority_queue<int> que;
    for(int i=1;i<=m;i++) {
        int u,v;
        cin>>u>>v;
        edge[v].push_back(u);
        in_deg[u]++;
    }
    for(int i=1;i<=n;i++) {
        if(in_deg[i]==0) que.push(i);
    }
    vector<int> ans;
    while(!que.empty()) {
        int u=que.top();
        ans.push_back(u);
        que.pop();
        for(int v:edge[u]) {
            in_deg[v]--;
            if(in_deg[v]==0) que.push(v);
        }
    }
    if(ans.size()!=n) {
        cout<<"Impossible!"<<endl;
    }
    else {
        reverse(ans.begin(),ans.end());
        for(int v:ans) cout<<v<<" ";
        cout<<endl;
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

## [[TJUT OJ] game](https://code.sipc115.com/problem/621)

诈骗题，以为是根据 SG 函数进行分类讨论，但是实际上可以构造出策略：一直拿max，都相等了再往下拿。这样的话就变成一个很纯的博弈模板了，注意特判初始状态是否符合题意。

```c
#include<stdio.h>
#include<stdlib.h>

void solve() {
    long long n,k;
    scanf("%lld%lld",&n,&k);
    long long *a=(long long*)malloc(sizeof(long long)*n);
    long long mx=-4e18,mn=4e18,sum=0,cnt=0;
    for(int i=0;i<n;i++) {
        scanf("%lld",&a[i]);
        if(a[i]>mx) {
            mx=a[i];
        }
        if(a[i]<mn) {
            mn=a[i];
        }
        sum+=a[i];
    }
    for(int i=0;i<n;i++) {
        if(a[i]==mx) cnt++;
    }
    if(mx-mn>k+1||(mx-mn==k+1&&cnt>1)) {
        printf("Bob\n");
    }
    else {
        if(sum%2==1) printf("Alice\n");
        else printf("Bob\n");
    }
    free(a);
}
signed main() {
    int T;
    scanf("%d",&T);
    while(T--) {
        solve();
    }
    return 0;
}
```

## [Bear and Strings](https://codeforces.com/contest/385/problem/B)

固定右端点的时候，假设 `p` 是最靠右的一个 `bear` 的起始下标，并且这个 `bear` 完全落在了当前子串范围内，那么：

- 任何 `l<=p` 都能包含 `bear`
- 任何 `l>p` 都不能包含 `bear`

所以我们直接双指针就行了，每次产生的贡献就是从 `last` 到当前位置。

```c++
#include<bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin>>s;
    int n=s.size(),last=0;
    s=" "+s;
    int ans=0;
    for(int r=4;r<=n;r++) {
        if(s[r]=='r'&&s[r-1]=='a'&&s[r-2]=='e'&&s[r-3]=='b') {
            last=r-3;
        }
        if(last!=0) {
            ans+=last;
        }
    }
    cout<<ans;
    return 0;
}
```

## [[BJOI2018] 求和](https://www.luogu.com.cn/problem/P4427)

这道题其实是有点树链剖分的感觉的，但是因为不在线，所以难度就大幅下降了。

利用树上前缀和，直接可以计算。

但是它有个 $k$，这可咋办？答案是分层维护，这样就做完了。

需要上快读，这里直接贴上我网络赛卡常用的快读喵。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
namespace Fastio{struct Reader{template<typename T>Reader&operator>>(T&x){x=0;short f=1;char c=getchar_unlocked();while(c<'0'||c>'9'){if(c=='-')f*=-1;c=getchar_unlocked();}while(c>='0'&&c<='9')x=(x<<3)+(x<<1)+(c^48),c=getchar_unlocked();x*=f;return*this;}Reader&operator>>(double&x){x=0;double t=0;short f=1,s=0;char c=getchar_unlocked();while((c<'0'||c>'9')&&c!='.'){if(c=='-')f*=-1;c=getchar_unlocked();}while(c>='0'&&c<='9'&&c!='.')x=x*10+(c^48),c=getchar_unlocked();if(c=='.')c=getchar_unlocked();else{x*=f;return*this;}while(c>='0'&&c<='9')t=t*10+(c^48),s++,c=getchar_unlocked();while(s--)t/=10.0;x=(x+t)*f;return*this;}Reader&operator>>(long double&x){x=0;long double t=0;short f=1,s=0;char c=getchar_unlocked();while((c<'0'||c>'9')&&c!='.'){if(c=='-')f*=-1;c=getchar_unlocked();}while(c>='0'&&c<='9'&&c!='.')x=x*10+(c^48),c=getchar_unlocked();if(c=='.')c=getchar_unlocked();else{x*=f;return*this;}while(c>='0'&&c<='9')t=t*10+(c^48),s++,c=getchar_unlocked();while(s--)t/=10.0;x=(x+t)*f;return*this;}Reader&operator>>(__float128&x){x=0;__float128 t=0;short f=1,s=0;char c=getchar_unlocked();while((c<'0'||c>'9')&&c!='.'){if(c=='-')f*=-1;c=getchar_unlocked();}while(c>='0'&&c<='9'&&c!='.')x=x*10+(c^48),c=getchar_unlocked();if(c=='.')c=getchar_unlocked();else{x*=f;return*this;}while(c>='0'&&c<='9')t=t*10+(c^48),s++,c=getchar_unlocked();while(s--)t/=10.0;x=(x+t)*f;return*this;}Reader&operator>>(char&c){c=getchar_unlocked();while(c==' '||c=='\n'||c=='\r')c=getchar_unlocked();return*this;}Reader&operator>>(char*str){int len=0;char c=getchar_unlocked();while(c==' '||c=='\n'||c=='\r')c=getchar_unlocked();while(c!=' '&&c!='\n'&&c!='\r')str[len++]=c,c=getchar_unlocked();str[len]='\0';return*this;}Reader&operator>>(std::string&str){str.clear();char c=getchar_unlocked();while(c==' '||c=='\n'||c=='\r')c=getchar_unlocked();while(c!=' '&&c!='\n'&&c!='\r')str.push_back(c),c=getchar_unlocked();return*this;}Reader(){}}cin;class the_endl{}endl;struct Writer{const int Setprecision=6;typedef int mxdouble;template<typename T>Writer&operator<<(T x){if(x==0){putchar_unlocked('0');return*this;}if(x<0)putchar_unlocked('-'),x=-x;static short sta[40];short top=0;while(x>0)sta[++top]=x%10,x/=10;while(top>0)putchar_unlocked(sta[top]+'0'),top--;return*this;}Writer&operator<<(double x){if(x<0)putchar_unlocked('-'),x=-x;mxdouble _=x;x-=(double)_;static short sta[40];short top=0;while(_>0)sta[++top]=_%10,_/=10;if(top==0)putchar_unlocked('0');while(top>0)putchar_unlocked(sta[top]+'0'),top--;putchar_unlocked('.');for(int i=0;i<Setprecision;i++)x*=10;_=x;while(_>0)sta[++top]=_%10,_/=10;for(int i=0;i<Setprecision-top;i++)putchar_unlocked('0');while(top>0)putchar_unlocked(sta[top]+'0'),top--;return*this;}Writer&operator<<(long double x){if(x<0)putchar_unlocked('-'),x=-x;mxdouble _=x;x-=(long double)_;static short sta[40];short top=0;while(_>0)sta[++top]=_%10,_/=10;if(top==0)putchar_unlocked('0');while(top>0)putchar_unlocked(sta[top]+'0'),top--;putchar_unlocked('.');for(int i=0;i<Setprecision;i++)x*=10;_=x;while(_>0)sta[++top]=_%10,_/=10;for(int i=0;i<Setprecision-top;i++)putchar_unlocked('0');while(top>0)putchar_unlocked(sta[top]+'0'),top--;return*this;}Writer&operator<<(__float128 x){if(x<0)putchar_unlocked('-'),x=-x;mxdouble _=x;x-=(__float128)_;static short sta[40];short top=0;while(_>0)sta[++top]=_%10,_/=10;if(top==0)putchar_unlocked('0');while(top>0)putchar_unlocked(sta[top]+'0'),top--;putchar_unlocked('.');for(int i=0;i<Setprecision;i++)x*=10;_=x;while(_>0)sta[++top]=_%10,_/=10;for(int i=0;i<Setprecision-top;i++)putchar_unlocked('0');while(top>0)putchar_unlocked(sta[top]+'0'),top--;return*this;}Writer&operator<<(char c){putchar_unlocked(c);return*this;}Writer&operator<<(the_endl en){putchar_unlocked('\n'),fflush(stdout);return*this;}Writer&operator<<(char*str){int cur=0;while(str[cur])putchar_unlocked(str[cur++]);return*this;}Writer&operator<<(const char*str){int cur=0;while(str[cur])putchar_unlocked(str[cur++]);return*this;}Writer&operator<<(std::string str){int st=0,ed=str.size();while(st<ed)putchar_unlocked(str[st++]);return*this;}Writer(){}}cout;}using namespace Fastio;
#define cin Fastio::cin
#define cout Fastio::cout
const int MOD = 998244353;
const int LOG = 31;
const int MAXN = 3e5+100;
#define endl '\n'

ll n,fa[MAXN][32],m,dep[MAXN][51],pre[MAXN][51];
bool vis[MAXN];
vector<ll> edge[MAXN];
queue<ll> que;

void dfs(int u,int f,int k) {
    for(int v:edge[u]) {
        if(v==f) continue;
        pre[v][k]=(pre[u][k]+dep[v][k])%MOD;
        dfs(v,u,k);
    }
}

int lca(int u,int v) {
    if(dep[v][1]>dep[u][1]) swap(u,v);
    for(int i=LOG;i>=0;i--) {
        if(fa[u][i]&&dep[fa[u][i]][1]>=dep[v][1]) {
            u=fa[u][i];
        }
    }
    if(u==v) return u;
    for(int i=LOG;i>=0;i--) {
        if(fa[u][i]!=fa[v][i]) {
            u=fa[u][i];
            v=fa[v][i];
        }
    }
    return fa[u][0];
}

int main() {
    cin>>n;
    for(int i=1;i<n;i++) {
        int u,v;
        cin>>u>>v;
        edge[u].push_back(v);
        edge[v].push_back(u);
    }
    que.push(1);
    vis[1]=true;
    while(!que.empty()) {
        int u=que.front();
        que.pop();
        for(int v:edge[u]) {
            if(vis[v]) continue;
            dep[v][1]=dep[u][1]+1;
            fa[v][0]=u;
            for(int j=1;j<=LOG;j++) {
                fa[v][j]=fa[fa[v][j-1]][j-1];
            }
            vis[v]=true;
            que.push(v);
        }
    }
    for(int i=1;i<=n;i++) {
        for(int j=2;j<=50;j++) {
            dep[i][j]=(dep[i][j-1]*dep[i][1])%MOD;
        }
    }
    for(int i=1;i<=50;i++) {
        pre[1][i]=dep[1][i];
        dfs(1,0,i);
    }
    cin>>m;
    while(m--) {
        int u,v,k;
        cin>>u>>v>>k;
        ll ans;
        int w=lca(u,v);
        ans=(((((pre[u][k]+pre[v][k])%MOD)-2*pre[w][k])%MOD)+dep[w][k])%MOD;
        ans=(ans%MOD+MOD)%MOD;
        cout<<ans<<endl;
    }
    return 0;
}
```

## [Minimum Notation](https://codeforces.com/contest/1730/problem/C)

有题可知我们应该要把大的数字尽可能放到后面去，小的数字尽可能放到前面去。

每次执行完一次操作，都会有一个数字变大，那么我们一次操作是不是更优来就看它能不能放在字符串后面然后让一个更小的数字顶到前面来就行了。

根据我们这样推导，会发现一个数要被删除当且仅当它的后面有比它更小的数。有点单调栈的感觉，但其实只需要我们维护一个后缀最小值就可以解决了，把当前值和后缀最小值做个比较。

这里有个技巧就是我们不需要真的操作字符串，如果一个数应该删的话我们就给它加 1，最后答案的字典序要想最小那肯定是单调不减的，所以我们最后统一排序就行了。

```c++
#include<bits/stdc++.h>
#include <iostream>
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
    int mn=0x7f7f7f7f;
    vector<int> a(n);
    for(int i=0;i<n;i++) a[i]=s[i]-'0';
    for(int i=n-1;i>=0;i--) {
        if(a[i]>mn) a[i]=min(a[i]+1,9);
        mn=min(a[i],mn);
    }
    sort(a.begin(),a.end());
    for(int i=0;i<n;i++) cout<<a[i];
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

##

通过这道题联想到了上面熊那道题，其实本质差不多的。

因为 $n$ 和 $k$ 都是 $2e5$，我们可以直接动态维护，用一个 `set` 维护前缀和是否有这个数，用 `map` 维护出现的位置。

因为 $a_i > 0$，接下来只需要枚举 $k$ 的多少倍就行。

但是显然这个做法会 TLE，怎么办呢？

注意到上面的条件等价于存在前缀下标 $i<j$,满足$j-i>k$且$pre_i \equiv pre_j \pmod k$。

为什么呢？因为 $a_i>0$，前缀和严格递增，每个值只出现一次，枚举右端点 $j$ 把已经足够远的前缀余数丢进去，其实就是刚刚思路的逆向处理。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    ll n,k;
    cin>>n>>k;
    vector<ll> pre(n+1,0);
    for(int i=1;i<=n;i++) {
        ll x;
        cin>>x;
        pre[i]=pre[i-1]+x;
    }
    vector<ll> cnt(k,0);
    ll ans=0;
    for(int j=1;j<=n;j++) {
        int i=j-k-1;
        if(i>=0) ++cnt[pre[i]%k];
        ans+=cnt[pre[j]%k];
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

## [What's the Capital of France?](https://codeforces.com/problemset/problem/2261/B)

位运算好题。这种让我们维护按位或最值肯定是贪心，从最大的一位开始贪心，我们读读题看看操作本质是什么。

我们发现这个操作虽然是只能相邻操作，但是实际上我们如果指定一个格子，我们可以通过不断移动它的左右把它抬升到它本身到最大值之间的任何一个数字。这启发我们可以直接贪心构造一个与最大值互补（二进制位下）的数，让它们与完了是最值的二进制位下全是 1。但是交了一发 $WA$ 了，为什么呢？因为不一定能构造出来这样互补的，比如说 `1010110` 和 `1010101`，前面的那几位其实是动不了的。所以我们借助位运算 $O(log V)$ 算出可以动的首个位置，然后直接构造后面互补就结束了。

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
    vector<ll> a(n+1);
    ll mx=-INF,mn=INF;
    bool flag=false;
    for(int i=1;i<=n;i++) {
        cin>>a[i];
        mx=max(a[i],mx);
        mn=min(a[i],mn);
    }   
    int tbit=0;
    for(int i=31;i>=0;i--) {
        if(((mx>>i)&1)!=((mn>>i)&1)) {
            tbit=i+1;
            break;
        }
    }
    ll ans=(mx>>(tbit)<<(tbit))+(1<<(tbit))-1;
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

## [Value Counters](https://codeforces.com/contest/2290/problem/F)

新鲜出炉的 div.4 题目。由题，我们可以把 $b_x$ 拆贡献。

设 $L_x$ 为比 $x$ 要小且排列在 $x$ 左边的数的个数，$R_x$ 为比 $x$ 大且排列在 $x$ 右边的数的个数，那么有：

$$b_x = L_x-R_X$$

设 $x$ 所在位置为 $pos_x$，看一看 $x$ 右边有哪些数，显然一共有 $n-pos_x$ 个数字在 $x$ 右边，观察：

$$n-pos_x=(x-1-L_x)+R_x$$

这个式子中，$x$ 右边的数分成两类，比 $x$ 小和比 $x$ 大，比 $x$ 小的数一共有 $x-1$ 个，其中有 $L_x$ 个在 $x$ 左边；比 $x$ 大的数字一共有 $R_x$ 个。

显然，$R_x-L_x$ 其实就是 $-b_x$，于是我们换掉，得：

$$n-pos_x=x-1-b_x$$

$b_x$ 是题目输入的，$n$ 也是我们已知的，我们反解 $pos_x$ 即可。

```c++
#include<bits/stdc++.h>
using namespace std;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    vector<int> b(n+1,0),pos(n+1,-1),has(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>b[i];
    }
    bool flag=true;
    for(int i=1;i<=n;i++) {
        pos[i]=n-i+1+b[i];
        if((pos[i]>n)||pos[i]<1) flag=false;
        else has[pos[i]]=true;
    }
    for(int i=1;i<=n;i++) {
        if(!has[i]) flag=false;
    }
    if(flag) {
        vector<int> ans(n+1);
        for(int i=1;i<=n;i++) {
            ans[pos[i]]=i;
        }   
        for(int i=1;i<=n;i++) {
            cout<<ans[i]<<" ";
        }
        cout<<endl;
    }
    else cout<<-1<<endl;
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

## [Even Subarrays](https://codeforces.com/problemset/problem/1731/C)

诈骗题，有个经典的 trick 可以解决这个问题。

> 一个数的约数个数为奇数等价于这个数是完全平方数。

所以其实就是找异或和为完全平方数的子数组个数。但是直接维护也有点麻烦，考虑正难则反，答案就是：

$$子数组总数- XOR 为完全平方数的子数组数$$

后者显然可以用前缀 XOR 维护，具体地说，令：

$$p_i=\oplus_{1}^{i},p_0=0$$

那么区间 $[l,r]$ 的 XOR 为：

$$p_r \oplus p_{l-1}$$

枚举右端点 $r$，我们要统计之前有多少个 $l$ 满足这个式子为完全平方数，其实就是等价于：

$$p_{l-1}=p_r \oplus k^2$$

所以维护一个数组 `cnt[x]`，表示之前某个前缀 XOR 值等于 $x$ 的次数。对于当前的 `p`，枚举所有可能的完全平方数 `k*k`，把 `cnt[p ^ (k*k)]` 累加到“坏区间”数量里。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define endl '\n'

void solve() {
    ll n;
    cin>>n;
    int lim=1;
    while(lim<=n) lim<<=1;
    // lim 是大于 n 的最小 2 的幂
    vector<ll> cnt(lim,0);
    cnt[0]=1;
    ll pre=0,bad=0;
    for(int i=1;i<=n;i++) {
        ll x;
        cin>>x;
        pre^=x;
        for(int k=0;1LL*k*k<lim;k++) {
            bad+=cnt[pre^(k*k)];
        }
        cnt[pre]++;
    }
    ll total=1LL*n*(n+1)/2;
    cout<<total-bad<<endl;
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

