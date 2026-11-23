// Confirmatory PiPrimes validation for modulus 9103, independent digit continuations.
// C++17: g++ -O3 -std=c++17 experiments/validate_9103.cpp -o validate_9103
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int P = 9103;
constexpr std::uint64_t BASE = 1000000000000000000ULL;
constexpr std::uint64_t ACCEPT = 18000000000000000000ULL;
constexpr std::uint64_t SEED = 910320261123ULL;
constexpr int TRIALS = 9999;
struct UniformDigits {
    std::mt19937_64 gen{SEED};
    std::uint64_t available = 0;
    int remaining = 0;
    int next() {
        if (!remaining) {
            std::uint64_t x;
            do { x = gen(); } while (x >= ACCEPT);
            available = x % BASE;
            remaining = 18;
        }
        const int result = static_cast<int>(available % 10);
        available /= 10;
        --remaining;
        return result;
    }
};
int multiplicative_order() {
    int k = 0, x = 1;
    do { x = x * 10 % P; ++k; } while (x != 1);
    return k;
}
struct Summary { std::uint64_t hits = 0; int residue = 0; int phase = 0; };
Summary scan_string(const std::string& digits, int begin, int end, int residue,
                    int phase, const std::vector<int>& weights) {
    std::uint64_t hits = 0;
    const int k = static_cast<int>(weights.size());
    for (int i = begin; i < end; ++i) {
        residue = (residue + (digits[i] - '0') * weights[phase]) % P;
        phase = (phase + 1 == k) ? 0 : phase + 1;
        hits += (residue == 0);
    }
    return {hits,residue,phase};
}
std::uint64_t scan_control(int M, int residue, int phase,
                            const std::vector<int>& weights, UniformDigits& rng) {
    std::uint64_t hits = 0;
    const int k = static_cast<int>(weights.size());
    for (int i = 0; i < M; ++i) {
        residue = (residue + rng.next() * weights[phase]) % P;
        phase = (phase + 1 == k) ? 0 : phase + 1;
        hits += (residue == 0);
    }
    return hits;
}
}
int main(int argc,char** argv) {
    try {
        if (argc != 4) {
            std::cerr << "Usage: validate_9103 DIGITS.txt TRAIN_END VALIDATION_END\n";
            return 2;
        }
        const int train_end = std::stoi(argv[2]), validation_end = std::stoi(argv[3]);
        if (train_end < 1 || validation_end <= train_end)
            throw std::invalid_argument("invalid train / validation boundaries");
        std::ifstream input(argv[1]);
        if (!input) throw std::runtime_error("cannot read digits file");
        std::string digits, line;
        while (std::getline(input, line)) {
            for (char c: line) {
                if (c >= '0' && c <= '9') digits += c;
                else if (c != '\r' && c != '.' && c != ' ' && c != '\t')
                    throw std::runtime_error("non-digit content in file");
            }
        }
        if (static_cast<int>(digits.size()) != validation_end || digits.substr(0,2) != "31")
            throw std::runtime_error("digits length or prefix mismatch");
        const int k = multiplicative_order();
        std::vector<int> weights(k);
        weights[0] = 1;
        for (int i=1; i<k; ++i) weights[i] = weights[i-1] * 10 % P;
        const Summary train = scan_string(digits,0,train_end,0,0,weights);
        const Summary observed = scan_string(digits,train_end,validation_end,train.residue,train.phase,weights);
        UniformDigits rng;
        std::vector<std::uint64_t> sample;
        sample.reserve(TRIALS);
        const int M = validation_end - train_end;
        std::uint64_t exceed = 0;
        long double sum = 0, sum2 = 0;
        for (int i=0; i<TRIALS; ++i) {
            auto h = scan_control(M,train.residue,train.phase,weights,rng);
            sample.push_back(h); sum += h; sum2 += (long double)h*h;
            exceed += h >= observed.hits;
        }
        std::sort(sample.begin(),sample.end());
        const long double avg = sum / TRIALS;
        const long double sd = std::sqrt(std::max((long double)0,sum2/TRIALS-avg*avg));
        auto percentile = [&](double q) { return sample[static_cast<std::size_t>(q * (TRIALS - 1))]; };
        std::cout << std::fixed << std::setprecision(8)
            << "{\n  \"modulus\": " << P << ",\n  \"train_end\": " << train_end
            << ",\n  \"validation_start\": " << (train_end+1)
            << ",\n  \"validation_end\": " << validation_end
            << ",\n  \"test_positions\": " << M
            << ",\n  \"training_residue\": " << train.residue
            << ",\n  \"period\": " << k
            << ",\n  \"observed_hits\": " << observed.hits
            << ",\n  \"iid_expected_hits\": " << static_cast<long double>(M)/P
            << ",\n  \"control_trials\": " << TRIALS
            << ",\n  \"seed\": " << SEED
            << ",\n  \"control_mean\": " << avg
            << ",\n  \"control_sd\": " << sd
            << ",\n  \"control_min\": " << sample.front()
            << ",\n  \"control_q025\": " << percentile(.025)
            << ",\n  \"control_median\": " << percentile(.5)
            << ",\n  \"control_q975\": " << percentile(.975)
            << ",\n  \"control_max\": " << sample.back()
            << ",\n  \"controls_greater_equal\": " << exceed
            << ",\n  \"one_sided_p\": " << static_cast<long double>(exceed+1)/(TRIALS+1)
            << ",\n  \"reject_at_001\": " << ((exceed+1)*100 <= (TRIALS+1) ? "true" : "false")
            << "\n}\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 2;
    }
}