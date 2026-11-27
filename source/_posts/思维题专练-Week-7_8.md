---
title: "思维题专练 Week 7-8"
description: "整理一些思维与构造题，树木又进步了喵～"
cover: /img/covers/acg-014.jpg
date: 2026-11-27 22:00:00
categories:
  - 算法竞赛
tags:
  - 专项练习
  - 构造
math: true
---

## 前言

这周继续做一些 trick 和 dp 和 贪心。

## [Diverse String](https://codeforces.com/contest/2285/problem/B)

假设有 $m$ 个 $1$，我们显然可以选择任意的两个 $1$ 所在的位置，然后把这个区间改成 $0$。不同的连续段删掉 $1$ 后得到的字符串一定是不同的，而且还可以选择一个单点修改成 $0$，总方案数为 $\frac{m(m+1)}{2}$。同理，有 $n-m$ 个 $0$，总方案数为 $\frac{(n-m)(n-m+1)}{2}$。

所以有 $m$ 个 $1$ 的时候，答案为：

$$1+\frac{m(m+1)}{2}+\frac{(n-m)(n-m+1)}{2}$$

这是一个关于 $m$ 的二次函数，且开口向上，所以在给定区间内，最大值一定在端点取得。

最多翻转 $k$ 次，设初始 $1$ 的个数为 $c$，最终 $1$ 的个数可以是区间 $[min(0,c-k),max(n,c+k)]$ 内的任意一个数，所以答案就是端点的函数值取最大值。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define int ll
#define endl '\n'

int n,m;

int D(int m) {
    return 1+m*(m+1)/2+(n-m)*(n-m+1)/2;
}

void solve() {
    string s;
    int k;
    cin>>n>>k;
    cin>>s;
    m=0;
    for(int i=0;i<n;i++) {
        if(s[i]=='1') m++;
    }
    int L=max(0LL,m-k);
    int R=min(n,m+k);
    int ans=max(D(L),D(R));
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

## [Cyclic MEX](https://codeforces.com/contest/1905/problem/D)



## [Max Substitution](https://codeforces.com/contest/2285/problem/C)

这道题只和唯一的最大元素有关，与它所在的位置无关，且数据范围允许我们排序，所以我们先从大到小排序一下观察一些性质。

注意到排序后，如果存在 $a_s=a_{s+1}$，那么这两个元素都无法修改，且位置在这两个数后面的都无法修改。原因很简单，如果前面都修改完了， $a_s$ 和 $a_{s+1}$ 同为最大值，不满足唯一性，而在他们后面的就不可能成为最大值了。

另外，如果最终数组改变了前 $j$ 个位置，那么第 $j$ 大的元素一定被改过，因为在它被修改的时候，它当前值 $\le a_j$，且它是唯一最大值，所以其他位置都严格小于 $a_j$，最终值只会更小，因此：

$$b_1,b_2,b_3,...,b_j<a_j$$

也就是说，前 $j$ 个位置只能取 $1,2,...,a_j-1$。

接下来反过来构造，对于任意的 $j \le r$，如果前 $j$ 个位置都取 $[1,a_j-1]$ 中的数，其他位置都不变，这是一定可以构造出来的。

具体地说，采用如下方法构造：

> 从 $1$ 开始扫，此时 $a_i$ 为唯一最大值，前面为 $<a_j\le a_i$ 直接把 $a_i$ 改成目标值，后面最大值 $a_{i+1}<a_i$，一点一点处理到第 $j$ 个位置。

也就是说，前 $j$ 个数，每个数有 $a_j-1$ 种可选，根据乘法原理，方案数为： $(a_j-1)^j$，累加求和即可。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define int ll
const int MOD = 1e9 + 7;
#define endl '\n'

bool cmp(int a,int b) {
    return a>b;
}
int qpow(int a,int b,int mod) {
    int res=1;
    while(b) {
        if(b&1) res=(res*a)%mod;
        a=(a*a)%mod;
        b>>=1;
    }
    return res;
}
void solve() {
    int n;
    cin>>n;
    vector<int> a(n);
    for(int i=0;i<n;i++) {
        cin>>a[i];
    }
    int ans=1; //原始数组
    sort(a.begin(),a.end(),cmp);
    for(int i=0;i<n;i++) {
        if(i+1<n&&a[i]==a[i+1]) break;
        ans=(ans+qpow(a[i]-1,i+1,MOD))%MOD;
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

## [Get an Even String](https://codeforces.com/contest/1660/problem/C)

有点类似于栈括号匹配的思想，如果能两个字母匹配的话，它们中间的部分是都要删除的，维护一个桶就行了。

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
    vector<int> cnt(26,0);
    int ans=s.size();
    for(int i=0;i<s.size();i++) {
        cnt[s[i]-'a']++;
        if(cnt[s[i]-'a']==2) {
            ans-=2;
            for(int j=0;j<26;j++) cnt[j]=0;
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

## [LR-remainders](https://codeforces.com/contest/1932/problem/C)

其实可以线段树暴力过的（x），但是太麻烦了，想想正解。正着维护发现其实不太好维护，因为模意义下除法要用逆元，而且还有可能模出来得到 0 很难处理。考虑正难则反，我们可以根据给定的 $s$ 算出这个序列的最后一个数是谁，然后把删数的操作看成倒着往里面插入数，再倒叙输出答案。其实类似的思想还有删边可以倒着处理成连边然后并查集维护图论的题。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    ll n,m;
    cin>>n>>m;
    vector<ll> a(n,0);
    for(int i=0;i<n;i++) {
        cin>>a[i];
    }
    string s;
    cin>>s;
    int pos=0;
    for(int i=0;i<s.size()-1;i++) {
        if(s[i]=='L') pos++;
    }
    vector<ll> ans;
    ans.push_back(a[pos]%m);
    ll pre=a[pos]%m;
    int R=pos,L=pos;
    for(int i=s.size()-2;i>=0;i--) {
        if(s[i]=='R') pre=(pre*(a[++R])%m)%m;
        else pre=(pre*(a[--L])%m)%m;
        ans.push_back(pre);
    }
    reverse(ans.begin(),ans.end());
    for(ll v:ans) cout<<v<<" ";
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

## [Longest Strike](https://codeforces.com/contest/1676/problem/F)

思维题，本来以为是动态规划之类的。实际上我们可以把所有出现次数大于 $k$ 的都预处理出来，然后放到一个 `vector` 里面，这样显然就变成了一个求最长连续区间的问题了。但是 $a_i$ 的值域太大了，肯定要离散化或者用哈希表存的，这里我们直接用 `map` 降低代码量。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n,k;
    cin>>n>>k;
    vector<int> a(n);
    map<int,int> mp;
    for(int i=0;i<n;i++) {
        cin>>a[i];
        mp[a[i]]++;
    }
    vector<int> v;
    for(auto it=mp.begin();it!=mp.end();it++) {
        if((*it).second>=k) {
            v.push_back((*it).first);
        }
    }
    if(v.empty()) {
        cout<<-1<<endl;
        return;
    }
    sort(v.begin(),v.end());
    int mx=0,L=v[0],R=v[0],tmp=v[0];
    for(int i=1;i<v.size();i++) {
        if(v[i]==v[i-1]+1) {
            if(mx<v[i]-tmp) {
                mx=v[i]-tmp;
                L=tmp;
                R=v[i];
            }
        }
        else {
            tmp=v[i];
        }
    }
    cout<<L<<" "<<R<<endl;
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

## [[ICPC 2019 Nanchang R] And and Pair](https://www.luogu.com.cn/problem/P17806)

不愧是区域赛题目啊，差点签到失败了呜呜呜。拿到题根据 $i\&j=0$ 这个性质简单尝试一下，发现如果固定下 $i$ 的话，假设它的最高位在 $p$ 位，因为 $j \le i$，所以 $j$ 在第 $p$ 位以上全都得是 $0$，而 $i\&j=0$ 所以第 $p$ 位也得是 $0$。在第 $p$ 位以下，如果 $i$ 的某一位是 $1$ 它的位就被定下来了，而如果 $i$ 的某一位是 $0$ 的话则有两个可以选的，然后就变成一个组合数问题了。

这里第一想法是居然固定 $i$ 后就可以通过组合数学计算 $j$ 的可能性，那么我对每个可能的 $i$ 都算一下，然后根据加法原理就做完了。

实际上，这样想是错误的，因为 $|S| \le 10^5$，而不是数，这样的话如果每个二进制位都是 $1$ 的话就直接指数爆炸了。

那么我们换个角度，我们如果固定住 $i$ 的最高位 $p$ 呢？，由于 $i\&n=i$，那么 $n_p$ 一定是 $1$，对下面的位数进行一些讨论。考虑第 $b$ 位，如果 $n_b=0$，由于 $i\&n=i$，这一位它如果是 $1$ 的话显然等式就不成立了，所以 $i_b=0$，而因为 $i\&j=0$，此时 $j_b$ 有两种选法，所以贡献是  $2$。

如果 $n_b=1$，那么 $i_b$ 有两种选择，如果 $i_b=0$，那么 $j_b$ 有两种选择，如果 $i_b=1$，那么 $j_b$ 只能是  $0$，贡献是 $3$。

设 $p$ 以下位 $n$ 中 $0$ 的个数为 $z_p$ 个，1 的个数为 $o_p$ 个，那么所有的最高位为 $p$ 的 $i$ 的总贡献就是：

$$ans=1+\sum_{p:n_p=1}2^{z_p}3^{o_p}$$ 

其中因为存在 $(0,0)$，所以需要加上 $1$。接下来直接按位算贡献累加，就能得到答案了，不要忘记取模。

实现的时候从低位往高位扫，维护一个乘积：

- 遇到 0 就乘 2
- 遇到 1 就先累加进答案再乘 3

这样的话在处理某一位之前，正好等于这一位以下所有位的 $2^z+3^o$。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
#define endl '\n'

void solve() {
    string s;
    cin>>s;
    ll ans=1,val=1;
    for(int i=s.size()-1;i>=0;i--) {
        if(s[i]=='1') {
            ans=(ans+val)%MOD;
            val=val*3%MOD;
        }
        else {
            val=val*2%MOD;
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

## [Same Count One](https://codeforces.com/problemset/problem/1774/D)

手玩一下，可行性其实很好判断，因为可以想怎么换怎么换，所以只要是 $1$ 的总数是 $n$ 的倍数就一定能平均分出去。

问题在于如何用最小的交换次数，这个其实也很好想到贪心的策略，就是把多 $1$ 的数组中的 $1$，分给少 $1$ 的数组（某一位多 $1$ 的数组恰好是 $1$ 而少 $1$ 的数组恰好是 $0$ 的时候）。

实现可能有点麻烦，但是因为题目保证了 $nm\le10^6$，所以可以写两个 `vector` 来存一下，再模拟交换就行了。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

struct Node {
    int x,y,z;
};

void solve() {
    int n,m;
    cin>>n>>m;
    int sum=0;
    vector<vector<int>> a(n,vector<int>(m));
    vector<int> cnt(n);
    for(int i=0;i<n;i++) {
        int tmp=0;
        for(int j=0;j<m;j++) {
            cin>>a[i][j];
            sum+=a[i][j],tmp+=a[i][j];
        }
        cnt[i]=tmp;
    }
    if(sum%n!=0) {
        cout<<-1<<endl;
        return;
    }
    int t=sum/n;
    vector<Node> ans;
    vector<int> tmpa,tmpb;
    for(int j=0;j<m;j++) {
        tmpa.clear(),tmpb.clear();
        for(int i=0;i<n;i++) {
            if(cnt[i]>t&&a[i][j]==1) tmpa.push_back(i);
            if(cnt[i]<t&&a[i][j]==0) tmpb.push_back(i);
        }
        for(int i=0;i<min(tmpa.size(),tmpb.size());i++) {
            ans.push_back({tmpa[i]+1,tmpb[i]+1,j+1});
            cnt[tmpa[i]]--,cnt[tmpb[i]]++;
        } 
    }
    cout<<ans.size()<<endl;
    for(int i=0;i<ans.size();i++) {
        cout<<ans[i].x<<" "<<ans[i].y<<" "<<ans[i].z<<endl;
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

## [Special Permutation](https://codeforces.com/problemset/problem/1352/G)

简单构造题，注意到 $4$ 到 $1$ 的距离是 $3$，而 $2$ 到 $6$ 的距离是 $4$，所以直接让它奇数单调下降，然后用 $4、2、6$ 衔接一下再让偶数单调上升就做完了。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

struct Node {
    int x,y,z;
};

void solve() {
    int n,m;
    cin>>n>>m;
    int sum=0;
    vector<vector<int>> a(n,vector<int>(m));
    vector<int> cnt(n);
    for(int i=0;i<n;i++) {
        int tmp=0;
        for(int j=0;j<m;j++) {
            cin>>a[i][j];
            sum+=a[i][j],tmp+=a[i][j];
        }
        cnt[i]=tmp;
    }
    if(sum%n!=0) {
        cout<<-1<<endl;
        return;
    }
    int t=sum/n;
    vector<Node> ans;
    vector<int> tmpa,tmpb;
    for(int j=0;j<m;j++) {
        tmpa.clear(),tmpb.clear();
        for(int i=0;i<n;i++) {
            if(cnt[i]>t&&a[i][j]==1) tmpa.push_back(i);
            if(cnt[i]<t&&a[i][j]==0) tmpb.push_back(i);
        }
        for(int i=0;i<min(tmpa.size(),tmpb.size());i++) {
            ans.push_back({tmpa[i]+1,tmpb[i]+1,j+1});
            cnt[tmpa[i]]--,cnt[tmpb[i]]++;
        } 
    }
    cout<<ans.size()<<endl;
    for(int i=0;i<ans.size();i++) {
        cout<<ans[i].x<<" "<<ans[i].y<<" "<<ans[i].z<<endl;
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

## [Stoned Game](https://codeforces.com/problemset/problem/1396/B)

博弈论题目，注意到只能选择一堆取走一颗石子，在此基础上又加了一个不能取对手取得一样的堆的限制。

自己写了几个数，发现这个加上不能取对手取得一样的堆的限制对结果的影响似乎不明显，考虑极端情况，也就是某一堆特别多。

这种情况下，先手方一直选择特别多的这堆，可以把后手方所有能拿的石子消耗完，这样就先手必胜。

否则其实就是两个人一次性拿一个石子，谁输谁赢的博弈，直接对总数讨论奇偶性就做完了。

```c++
#include<bits/stdc++.h>
using namespace std;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    vector<int> a(n);
    for(int i=0;i<n;i++) {
        cin>>a[i];
    }
    sort(a.begin(),a.end());
    int sum=0;
    for(int i=0;i<n-1;i++) sum+=a[i];
    if(sum<a[n-1]) {
        cout<<"T"<<endl;
    }
    else {
        sum+=a[n-1];
        if(sum%2==1) cout<<"T"<<endl;
        else cout<<"HL"<<endl;
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

## [Reverse](https://codeforces.com/problemset/problem/1618/F)

居然有 2000 ？！？！

通过读题，试一下给我的性质，不难发现我们经过一次操作后一定会变成一个二进制下最左边是 1 且 最右边也是 1 的数。考虑更多次操作，发现到达这里之后再插入0 相当于没有插入，因为反转字符串后等于加了个前导 0，会被消除。动手写了下哪些是可到达的，发现可到达的一定是它本身或者它反转后左右两边随便添加 1，只需要判断这里面有没有 $y$ 就行了，用字符串模拟。

实现起来非常麻烦，直接删除前导多余 1 和后导多余 1 提交 $WA$ 了，看了看发现如果是 `111111` 这种形式的话没办法判断到底匹配上了没有，所以我们还得暴力枚举匹配位置，要求这个匹配：

- 匹配位置左边都是 1
- 匹配位置右边都是 1
- 匹配位置刚刚好等于中心串

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    ll x,y;
    cin>>x>>y;
    if(x==y) {
        cout<<"YES"<<endl;
        return;
    }
    string s,t;
    while(x) {
        s+=x%2+'0';
        x/=2;
    }
    while(y) {
        t+=y%2+'0';
        y/=2;
    }
    reverse(t.begin(),t.end());
    reverse(s.begin(),s.end());
    int k=(int)s.size()-1;
    while(k>=0&&s[k]=='0') {
        k--;
    }
    string ss;
    for(int i=0;i<=k;i++) {
        ss+=s[i];
    }
    string A;
    for(int i=(int)ss.size()-1;i>=0;i--) {
        A+=ss[i];
    }
    string rA=ss;
    string B="1";
    for(int i=(int)s.size()-1;i>=0;i--) {
        B+=s[i];
    }
    string rB=s+"1";
    string core[4]={A,rA,B,rB};
    bool flag=false;
    for(int id=0;id<4;id++) {
        for(int p=0;p<=(int)t.size();p++) {
            for(int q=0;q<=(int)t.size();q++) {
                string tmp;
                for(int i=0;i<p;i++) {
                    tmp+='1';
                }
                tmp+=core[id];
                for(int i=0;i<q;i++) {
                    tmp+='1';
                }
                if(tmp==t) {
                    flag=true;
                }
            }
        }
    }
    if(flag) {
        cout<<"YES"<<endl;
    }
    else {
        cout<<"NO"<<endl;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    while (T--) {
        solve();
    }
    return 0;
}
```

神秘代码，不喜勿喷（x）

## [k-Tree](https://codeforces.com/contest/431/problem/C)

考虑不在树上，容斥一下其实就是用 $1$ 到 $k$ 组成 $n$ 的方案数和用 $1$ 到 $d-1$ 组成 $n$ 的方案数的差，显然可以直接完全背包解决。

但是问题是现在我们在树上，$1+2$ 和 $2+1$ 会被认为是两种不同的路径，这该怎么办呢？其实就是做有序拆分，有序拆分和完全背包可以用类似的思想。

定义 $dp_j$ 表示总重量为 $j$ 的路径数，路径的边权序列有顺序。转移的时候枚举最后一条边：

$$dp[j] = \sum_{e=1}^{\min(j,k)} dp[j-e]$$

这其实就是：

```c++
for (int j = 1; j <= n; j++)          // 总重量在外
    for (int e = 1; e <= min(j, k); e++) // 最后一条边在内
        dp[j] += dp[j - e];
```

所以只要写一个 $k$ 层的有序拆分就行了。注意为了避免负数取模要加上个 $MOD$。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e2+100;
#define endl '\n'

ll dp[MAXN][MAXN],n,k,d;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n>>k>>d;
    for(int i=1;i<=k;i++) {
        dp[0][i]=1;
    }
    for(int t=1;t<=k;t++) {
        for(int j=1;j<=n;j++) {
            for(int i=1;i<=min(j,t);i++) {
                if(j>=i) {
                    dp[j][t]=(dp[j-i][t]%MOD+dp[j][t]%MOD)%MOD;
                }
            }
        }
    }
    cout<<(dp[n][k]-dp[n][d-1]+MOD)%MOD;
    return 0;
}
```

## [Productive Meeting](https://codeforces.com/contest/1579/problem/D)

观察样例，发现随便组合肯定是不行，想到应该让最大的两个人交流。

一开始考虑优化，让最大的人把此大的人用完，结果发现这样构造会有反例，那就暴力模拟吧。

具体来说，我们要维护全局最大和全局此大，且是动态的，这启发我们用大根堆。

实现起来比较麻烦，得处理编号。

```c++
#include<bits/stdc++.h>
using namespace std;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    priority_queue<pair<int,int>> que;
    for(int i=0;i<n;i++) {
        int x;
        cin>>x;
        if(x==0) continue;
        que.push({x,i+1});
    }
    vector<pair<int,int>> v;
    while(que.size()>=2) {
        auto [tmp1,id1]=que.top();
        que.pop();
        auto [tmp2,id2]=que.top();
        que.pop();
        tmp1--;
        tmp2--;
        if(tmp1>0) que.push({tmp1,id1});
        if(tmp2>0) que.push({tmp2,id2});
        v.push_back({id1,id2});
    }
    cout<<v.size()<<endl;
    for(auto [u,v]:v) {
        cout<<u<<" "<<v<<endl;
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

## [Zuma](https://codeforces.com/contest/607/problem/B)

考虑区间动态规划，设 $dp_{i,j}$ 表示删除区间 $[i,j]$ 的最小花费。显然的，有：

$$dp_{i,i}=1,dp_{i,i+1}=1 (a_i=a_{i+1}),dp_{i,i+1}=2(a_i\neq a_{i+1})$$

然后考虑转移，显然枚举分界点 $k$ 就可以，但是有个特殊情况，就是**如果两端颜色相同，最外层的两颗宝石可以和「内部最后被删掉的那块回文」拼在一起删**。

所以正确的转移是：

$$dp[l][r]=\min\Big(\min_{l\le k<r}\big(dp[l][k]+dp[k+1][r]\big),\ \ [c_l=c_r]\cdot dp[l+1][r-1]\Big)$$

这样就做完了。做这道题的时候懒得实现代码了就给 AI 大人了。

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> c(n);
    for (int &x : c) cin >> x;

    const int INF = 1e9;
    vector<vector<int>> dp(n, vector<int>(n, INF));
    for (int i = 0; i < n; ++i) dp[i][i] = 1;

    for (int len = 2; len <= n; ++len) {
        for (int l = 0; l + len - 1 < n; ++l) {
            int r = l + len - 1;

            // 两端同色：和内部最后一块一起删
            if (c[l] == c[r]) {
                dp[l][r] = (len == 2 ? 1 : dp[l + 1][r - 1]);
            }

            // 枚举分割点，左右独立删
            for (int k = l; k < r; ++k) {
                dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r]);
            }
        }
    }

    cout << dp[0][n - 1] << '\n';
    return 0;
}
```

## [Young Explorers](https://codeforces.com/contest/1355/problem/B)

简单小贪心，我们应该尽可能让一组正好全都是经验不足程度相同的，这样的话就可以一个组只放这么多人。但是考虑到会有剩下的，那就让剩下的跟剩下的继续建组，这里需要排序再模拟，为了降低码量可以用 $map$ 实现。

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
    vector<int> a(n);
    map<int,int> cnt;
    int lp=0;
    for(int i=0;i<n;i++) {
        cin>>a[i];
        cnt[a[i]]++;
    }
    int ans=0;
    for(auto [e,p]:cnt) {
        ans+=p/e;
        lp+=p%e;
        int ew=lp/e;
        ans+=ew;
        lp-=ew*e;
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

## [Quests](https://codeforces.com/contest/1760/problem/F)

注意到是最大中找最小，直接考虑二分答案，问题转化成了如何 $O(n)$ 判断能否在 $k$ 的情况下达到目标。

注意到所有任务都是隔 $k$ 天才行，所以我们可以找出前 $k+1$ 大，然后分配下去周期显然是 $k+1$，处理最后的余数就行了。这里可以用前缀和优化。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

ll n,d,c,a[MAXN],s[MAXN];

bool cmp(ll a,ll b) {
    return a>b;
}

bool check(ll k) {
    ll sum=0;
    ll inx=min(k+1,n);
    ll tmp=s[inx];
    sum+=d/(k+1)*tmp;
    sum+=s[min(n,d%(k+1))];
    return sum>=c;
}
void solve() {
    memset(a,0,sizeof(a));
    memset(s,0,sizeof(s));
    cin>>n>>c>>d;
    for(int i=1;i<=n;i++) {
        cin>>a[i];
    }
    sort(a+1,a+1+n,cmp);
    for(int i=1;i<=n;i++) {
        s[i]=s[i-1]+a[i];
    }
    if(check(INF)) {
        cout<<"Infinity"<<endl;
        return;
    }
    if(!check(0)) {
        cout<<"Impossible"<<endl;
        return;
    }
    ll L=0,R=MAXN,ans=-1;
    while(L<=R) {
        ll mid=(L+R)>>1;
        if(check(mid)) {
            ans=mid;
            L=mid+1;
        }
        else {
            R=mid-1;
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

## [[蓝桥杯 2023 国 Python B] 翻转](https://www.luogu.com.cn/problem/P12211)

考虑正难则反，我们可以维护最多可以合并的数目，然后答案就是 $2n-mx$。

问题变成了怎么维护最多的可以合并的数目。注意到这个东西只和当前这个字符串是否反转和上一个字符串是否反转有关，我们可以进行线性递推，具体来说，因为字符串长度都是 $2$，所以其实有影响的只有 $4$ 个字母，分类讨论一下做动态规划就行了。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin>>n;
    vector<string> s(n);
    vector<int> dp(2);
    for(int i=0;i<n;i++) {
        cin>>s[i];
    }
    for(int i=1;i<n;i++) {
        char x0=s[i-1][0],y0=s[i-1][1];
        char x1=s[i][0],y1=s[i][1];
        int ndp0=max(dp[0]+(y0==x1?1:0),dp[1]+(x0==x1?1:0));
        int ndp1=max(dp[1]+(x0==y1?1:0),dp[0]+(y0==y1?1:0));
        dp[0]=ndp0,dp[1]=ndp1;
    }
    cout<<2*n-max(dp[1],dp[0]);
    return 0;
}
```

## [[蓝桥杯 2019 省 A] 修改数组](https://www.luogu.com.cn/problem/P8686)

直接模拟肯定是不行的，想到可以二分，但是玩了一下发现未必有单调性。再读一遍题发现 $A_i$ 值域比较小，直接开一个 `set` 全放进去，然后在 `set` 里面的表示没出现过的，然后动态删除就行了，用 `lower_bound` 实现二分。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 4e18;
const int MAXV = 1e6+100;
#define endl '\n'

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll n;
    cin>>n;
    set<ll> s;
    for(int i=1;i<=1e6;i++) {
        s.insert(i);
    }
    for(int i=0;i<n;i++) {
        ll x;
        cin>>x;
        if(s.count(x)) {
            s.erase(x);
            cout<<x<<" ";
        }
        else {
            auto it=s.lower_bound(x);
            cout<<*it<<" ";
            s.erase(it);
        }
    }
    return 0;
}
```

然而这样做有些太暴力了，看了看题解区有个做法我很喜欢，就是利用并查集， `find` 函数表示的是大于等于 $x$ 中的第一个还没被使用的数，显然初始化都是自己。当某个数 `v` 被占用（也就是已经写进答案）后，就令 `fa[v] = find(v + 1)`。这相当于在说：“`v` 已经不可用了，请把它对应到 `v+1` 的下一个可用位置去。”，然后查询就行了。

```c++
#include <bits/stdc++.h>
using namespace std;
const int MAXV = 1000000 + 100000 + 10;  // 最大可能值 maxA + N
int fa[MAXV];

int find(int x) {
    int r = x;
    while (fa[r] != r) r = fa[r];                 // 找根 = 第一个空位
    while (fa[x] != r) { int nx = fa[x]; fa[x] = r; x = nx; } // 路径压缩
    return r;
}

int main() {
    int n; scanf("%d", &n);
    for (int i = 0; i < MAXV; i++) fa[i] = i;
    for (int i = 0; i < n; i++) {
        int a; scanf("%d", &a);
        int v = find(a);       // v = >= a 的第一个没用过的数
        printf("%d ", v);
        fa[v] = find(v + 1);   // 占用 v，指向下一个空位
    }
    return 0;
}
```

## [[蓝桥杯 2014 省 B] 小朋友排队](https://www.luogu.com.cn/problem/P8613)

一个很好的 trick 题，读完题考虑到跟逆序对有关，毕竟一个数组的最小交换次数就是逆序对。但是这道题每个人每次交换产生的贡献都不一样，这样我们就不能简单维护逆序对了。考虑对逆序对本身拆贡献，我们会发现一个数对逆序对的二倍这个值的贡献是它左边比它大的数目加上它右边比它小的数目，而二倍的原因是因为 $(1,2)、(2,1)$ 这样的逆序对会算重复。这样拆贡献之后我们就可以用树状数组分两次维护，然后做出答案了。注意这道题因为身高有可能是 $0$，需要整体加上 $1$ 的偏移量，不然就会出现 `lowbit(0)=0` 从而死循环。

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
#define endl '\n'
const int MAXN = 1000000+100;

ll n,tree[MAXN],a[MAXN],ans;

ll lowbit(ll x) {
    return x&(-x);
}
void add(ll x,ll k) {
    for(int i=x;i<=MAXN;i+=lowbit(i)) {
        tree[i]+=k;
    }
}
ll query(ll x) {
    ll res=0;
    for(int i=x;i;i-=lowbit(i)) {
        res+=tree[i];
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n;
    for(int i=1;i<=n;i++) {
        cin>>a[i];
    }
    vector<ll> c(n+1);
    for(int i=1;i<=n;i++) {
        c[i]+=(ll)(i-1)-query(a[i]+1);
        add(a[i]+1,1);
    }
    memset(tree,0,sizeof(tree));
    for(int i=n;i>=1;i--) {
        c[i]+=query(a[i]);
        add(a[i]+1,1);
    }
    for(int i=1;i<=n;i++) ans+=(1LL+c[i])*c[i]/2;
    cout<<ans;
    return 0;
}
```

## [[蓝桥杯 2022 省 A] 选数异或](https://www.luogu.com.cn/problem/P8773)

本来以为是可持久化字典树，但是实现不出来。问了问 AI 发现并没有这么复杂。我们可以把每一对合法的数看成一个区间。

如果 $a_i \oplus a_j=x$ 且 $j<i$，就看成是区间 $[j,i]$，这样的话询问 $[l,r]$ 本质上就在问有没有一个合法区间 $[j,i]$ 被 $[l,r]$ 完全包含。

根据这个思想，我们需要对每个右端点，维护它最近的左端点。然后维护所有合法区间中最大的左端点。

假设当前扫到 $a_i$，想找它左边能和它配对的数，也就是 $a_j=a_i \oplus x$，这样的 $j$ 有很多个，但是如果最近的 $p_i<l$，那么更靠左的 $j$ 更小，也一定 $<l$，如果最近的 $p_i\ge l$，那就已经找到一组合法对 $(p_i,i)$ 了。所以只需要维护最近的左端点 $p_i$ 就足够了。

令 $f_i=\max(f_{i-1},p_i)$，它的含义是在所有右端点 $\le i$ 的合法区间 $[j,k]$ 中，最大的左端点 $j$ 的值，这样维护后，每次询问 $[l,r]$ 就是一个分类讨论。

- $f_r\ge l$，这时存在一个合法区间，它的左端点至少是 $l$，右端点又不超过 $r$，答案显然就是 `yes`。
- $f_r<l$，说明所有的合法区间左端点都小于 $l$。答案显然就是 `no`。

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, x;
    cin >> n >> m >> x;

    const int V = 1 << 20;
    vector<int> pos(V, 0);
    vector<int> f(n + 1, 0);

    for (int i = 1; i <= n; ++i) {
        int a;
        cin >> a;

        // 找能和 a 异或成 x 的数的最近位置
        int need = a ^ x;
        int p = pos[need];

        f[i] = max(f[i - 1], p);

        // 更新 a 的最后出现位置
        pos[a] = i;
    }

    while (m--) {
        int l, r;
        cin >> l >> r;
        cout << (f[r] >= l ? "yes\n" : "no\n");
    }

    return 0;
}
```

