// Build: g++ -O3 -std=c++17 experiments/modular_scan.cpp -o modular_scan
// Usage: modular_scan pi_digits.txt counts.csv [start=1] [max_prime=10000]
// Optional fifth positional argument: hit_indices.csv (or - to skip).
// Optional sixth positional argument: phase_diagnostics.csv (or - to skip).
// Does not construct enormous F_n. Uses bounded 32-bit modular arithmetic.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

static std::vector<int> primes_up_to(int ceiling) {
    std::vector<bool> composite(ceiling + 1);
    for (int i = 2; 1LL*i*i <= ceiling; ++i)
        if (!composite[i]) for (int j = i*i; j <= ceiling; j += i) composite[j] = true;
    std::vector<int> primes;
    for (int i = 3; i <= ceiling; i += 2) if (!composite[i] && i != 5) primes.push_back(i);
    return primes;
}
static int order10(int p) {
    int power=1, order=0;
    do {power=power*10%p;++order;} while (power!=1);
    return order;
}
int main(int argc, char** argv) {
    try {
        if (argc < 3 || argc > 7) {
            std::cerr << "Usage: modular_scan DIGITS.txt COUNTS.csv [START=1] [MAX_PRIME=10000] [HITS.csv|-] [PHASE.csv|-]\n";
            return 2;
        }
        const int start = argc > 3 ? std::stoi(argv[3]) : 1;
        const int limit = argc > 4 ? std::stoi(argv[4]) : 10000;
        if (limit < 3 || limit > 1000000) throw std::invalid_argument("MAX_PRIME must be 3..1000000");
        std::ifstream in(argv[1], std::ios::binary);
        if (!in) throw std::runtime_error("cannot open input digits");
        std::string digits, line;
        while (std::getline(in, line)) {
            for (char c : line) {
                if (c >= '0' && c <= '9') digits.push_back(c);
                else if (c != '\r' && c != ' ' && c != '\t' && c != '.')
                    throw std::runtime_error("non-digit in input");
            }
        }
        const int n = static_cast<int>(digits.size());
        if (start < 1 || start > n) throw std::invalid_argument("START must lie in 1..N");
        std::ofstream out(argv[2]);
        if (!out) throw std::runtime_error("cannot open output CSV");
        std::ofstream hits;
        if (argc > 5 && std::string(argv[5]) != "-") {
            hits.open(argv[5]);
            if (!hits) throw std::runtime_error("cannot open hits CSV");
            hits << "prime,n,phase\n";
        }
        std::ofstream phase_out;
        if (argc > 6 && std::string(argv[6]) != "-") {
            phase_out.open(argv[6]);
            if (!phase_out) throw std::runtime_error("cannot open phase CSV");
            phase_out << "prime,order10,arrival_phase,opportunities,hits,eligible_positions,eligible_digit_choices\n";
        }
        std::string hit_buffer;
        hit_buffer.reserve(1024*1024);
        out << "prime,order10,hits,tested,expected_approx,minimum_hits_phase,maximum_hits_phase,zero_hit\n";
        const auto primes=primes_up_to(limit);
        std::uint64_t missing=0, checked=0;
        for (int p : primes) {
            int residue=0, weight=1;
            const int k=order10(p);
            std::vector<std::uint32_t> phases(k,0), opportunities(k,0), eligible_positions(k,0), eligible_digit_choices(k,0);
            const bool detail=bool(phase_out) && (p==3 || p==7 || p==11 || p==13 || p==37 || p==41 || p==101);
            std::uint64_t count=0;
            for (int j=0; j<n; ++j) {
                const int digit = digits[j]-'0';
                if (detail && j+1>=start) {
                    const int phase=(j+1)%k;
                    ++opportunities[phase];
                    int choices=0;
                    for (int d=0;d<10;++d) choices+=((residue+d*weight)%p == 0);
                    eligible_positions[phase]+=choices>0;
                    eligible_digit_choices[phase]+=choices;
                }
                residue = (residue + digit*weight) % p;
                weight = (weight*10) % p;
                if (j+1 >= start && residue == 0) {
                    ++count;
                    ++phases[(j+1)%k];
                    if (hits) {
                        hit_buffer += std::to_string(p) + ',' + std::to_string(j+1) + ',' + std::to_string((j+1)%k) + '\n';
                        if (hit_buffer.size() > 1024*1024) {hits.write(hit_buffer.data(),hit_buffer.size());hit_buffer.clear();}
                    }
                }
            }
            if (detail) for (int phase=0;phase<k;++phase) {
                phase_out << p << ',' << k << ',' << phase << ',' << opportunities[phase] << ',' << phases[phase] << ',' << eligible_positions[phase] << ',' << eligible_digit_choices[phase] << '\n';
            }
            checked += count;
            missing += count == 0;
            auto range=std::minmax_element(phases.begin(),phases.end());
            out << p << ',' << k << ',' << count << ',' << (n-start+1) << ',' << std::setprecision(12)
                << double(n-start+1)/p << ',' << *range.first << ',' << *range.second << ',' << (count==0) << '\n';
        }
        if (hits && !hit_buffer.empty()) hits.write(hit_buffer.data(),hit_buffer.size());
        std::cout << "digits=" << n << " primes=" << primes.size()
                  << " start=" << start << " zero_hit_primes=" << missing
                  << " divisible_pairs=" << checked << '\n';
        return 0;
    } catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 2; }
}