// SA_Himmelblau.cpp : Este arquivo contém a função 'main'. A execução do programa começa e termina ali.

#pragma once
#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <math.h>
#include <cmath>
#include <algorithm>
#include <random>

using namespace std;

struct Sol
{
    int iter;
    double x;
    double y;
    double T;
    double ObjVal;
};

int main()
{
    ofstream arquivoSaida;
    arquivoSaida.open("Saida.txt", ios_base::trunc);

    for (int repl = 0; repl < 100; repl++)
    {
        std::mt19937 rng;
        int M = 350;              // número de temperaturas
        int N = 2000;             // número de soluções
        double T0 = 1000.0;       // temperatura inicial
        double alpha = 0.90;      // fator de redução da temperatura
        double x = 2.0;           // x
        double y = 1.0;           // y
        vector<Sol> sol;          // vetor de soluções
        double k = 0.1;           // fator de ajuste, que define o passo de variação em x e y
        std::uniform_real_distribution<double> uniformDistribution(0.0, 1.0);
        rng.seed(std::random_device()());

        for (int i = 0; i < M; i++)
        {
            Sol bestSolIter;
            // Iteração global do SA
            for (int j = 0; j < N; j++)
            {
                if (j == 0)
                {
                    bestSolIter.iter = i;
                    bestSolIter.x = x;
                    bestSolIter.y = y;
                    bestSolIter.T = T0;
                    bestSolIter.ObjVal = (x * x + y - 11) * (x * x + y - 11) + (x + y * y - 7) * (x + y * y - 7);
                }

                double rnd_x1 = uniformDistribution(rng);
                double rnd_x2 = uniformDistribution(rng);
                double step_size_x = 0.0;
                if (rnd_x1 > 0.5) step_size_x = k * rnd_x2;
                else step_size_x = -k * rnd_x2;

                double rnd_y1 = uniformDistribution(rng);
                double rnd_y2 = uniformDistribution(rng);
                double step_size_y = 0.0;
                if (rnd_y1 > 0.5) step_size_y = k * rnd_y2;
                else step_size_y = -k * rnd_y2;

                double x1 = x + step_size_x;
                double y1 = y + step_size_y;

                double ObjVal = (x * x + y - 11) * (x * x + y - 11) + (x + y * y - 7) * (x + y * y - 7);
                double ObjVal1 = (x1 * x1 + y1 - 11) * (x1 * x1 + y1 - 11) + (x1 + y1 * y1 - 7) * (x1 + y1 * y1 - 7);

                if (ObjVal1 < ObjVal)
                {
                    x = x1;
                    y = y1;

                    if (ObjVal1 < bestSolIter.ObjVal)
                    {
                        bestSolIter.iter = i;
                        bestSolIter.x = x;
                        bestSolIter.y = y;
                        bestSolIter.T = T0;
                        bestSolIter.ObjVal = ObjVal1;
                    }
                }
                else
                {
                    double rnd = uniformDistribution(rng);
                    long double formula = exp(-(ObjVal1 - ObjVal) / T0);
                    if (rnd < formula)
                    {
                        x = x1;
                        y = y1;
                    }
                }
            }
            sol.push_back(bestSolIter);
            T0 = T0 * alpha;
        }
        double min = 10000000;
        int iMin = 0;
        for (int i = 0; i < M; i++)
        {
            if (sol[i].ObjVal < min)
            {
                min = sol[i].ObjVal;
                iMin = i;
            }
            //cout << setw(3) <<  sol[i].iter << " " << setw(8) << sol[i].x << " " << setw(8) << sol[i].y << " " << setw(8) << sol[i].T << " " << setw(8) << sol[i].ObjVal << endl;
            //arquivoSaida << setw(3) << repl << " " << setw(3) <<  sol[i].iter << " " << setw(8) << sol[i].x << " " << setw(8) << sol[i].y << " " << setw(8) << sol[i].T << " " << setw(8) << sol[i].ObjVal << endl;
        }
        cout << setw(3) << sol[iMin].iter << " " << setw(8) << sol[iMin].x << " " << setw(8) << sol[iMin].y << " " << setw(8) << sol[iMin].T << " " << setw(8) << sol[iMin].ObjVal << endl;
        arquivoSaida << setw(3) << repl << " " << setw(3) << sol[iMin].iter << " " << setw(8) << sol[iMin].x << " " << setw(8) << sol[iMin].y << " " << setw(8) << sol[iMin].T << " " << setw(8) << sol[iMin].ObjVal << endl;
    }
    arquivoSaida.close();
    system("PAUSE");
}
