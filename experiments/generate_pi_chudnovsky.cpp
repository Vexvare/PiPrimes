// Interval-certified decimal digits of pi using GMP Chudnovsky binary splitting.
// Build: g++ -O3 -std=c++17 generate_pi_chudnovsky.cpp -lgmpxx -lgmp -o generate_pi
// Digits include the initial 3; prints digits to file, a machine-checkable
// proof certificate: lower and upper exact rational bounds share the floor.
#include <gmpxx.h>
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>

namespace {
const mpz_class A(13591409), B(545140134), Q_CONST("10939058860032000");
struct Terms { mpz_class p,q,t; };
Terms combine(Terms left,Terms right) {
    Terms out;
    out.t = left.t*right.q + left.p*right.t;
    out.p = left.p*right.p;
    out.q = left.q*right.q;
    return out;
}
Terms split(unsigned long from, unsigned long until) {
    if (until-from==1) {
        Terms r;
        if (from==0) {r.p=1;r.q=1;r.t=A;}
        else {
            const mpz_class k(from);
            r.p=(6*k-5)*(2*k-1)*(6*k-1);
            r.q=k*k*k*Q_CONST;
            r.t=r.p*(A+B*k);
            if (from%2) r.t=-r.t;
        }
        return r;
    }
    const auto mid=from+(until-from)/2;
    return combine(split(from,mid),split(mid,until));
}
}
int main(int argc,char** argv) {
    try {
        if(argc!=3) {std::cerr<<"Usage: generate_pi COUNT OUTPUT.txt\n";return 2;}
        const unsigned long digits=std::stoul(argv[1]);
        if(digits<2||digits>10000000)throw std::invalid_argument("digits count must be 2..10000000");
        // Chudnovsky converges by >14 decimal digits / term; use 30 extra.
        const unsigned long terms=(digits+100)/14+5;
        std::cerr<<"Computing "<<terms<<" Chudnovsky terms for "<<digits<<" digits\n";
        auto res=split(0,terms);
        // The first omitted term has sign (+) for even terms, (-) for odd terms.
        // The alternating tail magnitude is bounded by the omitted term.
        const mpz_class k(terms);
        const mpz_class next_p=(6*k-5)*(2*k-1)*(6*k-1);
        const mpz_class next_q=k*k*k*Q_CONST;
        const mpz_class next_t=res.p*next_p*(A+B*k);
        // Common denominator Q*next_q; lower/upper numerators of S=sum terms.
        const mpz_class denom=res.q*next_q;
        const mpz_class partial=res.t*next_q;
        mpz_class low_sum=partial,high_sum=partial;
        if(terms%2==0) high_sum+=next_t;
        else low_sum-=next_t;
        if (low_sum<=0)throw std::runtime_error("invalid series bound");
        mpz_class scale;
        mpz_ui_pow_ui(scale.get_mpz_t(),10,digits-1);
        // floor(scale*sqrt(10005)) via exact isqrt(10005*scale^2).
        const mpz_class sq=10005*scale*scale;
        mpz_class sq_floor;
        mpz_sqrt(sq_floor.get_mpz_t(),sq.get_mpz_t());
        // pi*scale > 426880*sqrt_floor*denom/high_sum
        // pi*scale < 426880*(sqrt_floor+1)*denom/low_sum
        const mpz_class lower=(426880*sq_floor*denom)/high_sum;
        const mpz_class upper=(426880*(sq_floor+1)*denom)/low_sum;
        if(lower!=upper)throw std::runtime_error("ambiguous decimal truncation: more terms/precision required");
        const std::string str=lower.get_str();
        if(str.size()!=digits||str.substr(0,2)!="31")throw std::runtime_error("incorrect output digits");
        std::ofstream out(argv[2]);
        if(!out) throw std::runtime_error("cannot open output file");
        out<<str<<'\n';
        std::cerr<<"Confirmed identical exact rational floor bounds; wrote "<<str.size()<<" digits\n";
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 2;}
}