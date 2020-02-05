#include <iostream>
#include <vector>
#include <string>
#include <fstream>

class Process {
public:
    Process(char* argv[]) {
        this->argv = argv;
    }

    void write(int i) {
        std::fstream file;
        file.open("testoutput.txt");
        file.seekg(0, std::ios_base::end);

        if (i == 0) {
            // if file is empty
            if (!file.tellg()) {
                file << i << ' ';
            }  
            else {
                file << '\n' << i << ' ';
            }
        }
        else {
            file << i << ' ';
        }

    }

    void shell() {
        std::ifstream file(argv[1]);
        std::string line;
        std::vector<std::string> tokens;
        int initial = 0;
        while (getline(file, line)) {
            tokens.clear();
            for (int i = 0; i < sizeof(line) / sizeof(line[0]); i++) {
                if (line[i] == ' ') {
                    tokens.push_back(line.substr(initial, i));
                }
            }

            for (std::string i : tokens){
                std::cout << i << std::endl;
            }
        }
    }

private:
    std::vector<int> PCB;
    std::vector<int> RCB;
    std::vector<int> RL;
    int currentProcess;
    char** argv;
};

int main(int argc, char* argv[]) {
    Process run(argv);

    run.shell();
    return 0;
}