#include <stdio.h>

#define ARRAY_SIZE 10

int main() {
    int vector[ARRAY_SIZE];
    int scelta;

    // Menù migliorato
    printf("=========================================\n");
    printf("            PROGRAMMA VETTORE\n");
    printf("=========================================\n");
    printf("Scegli una delle seguenti opzioni:\n");
    printf("1 - Esegui programma corretto\n");
    printf("2 - Causa errore di segmentazione\n");
    printf("-----------------------------------------\n");
    printf("Inserisci la tua scelta: ");
    scanf("%d", &scelta);
    printf("=========================================\n");

    // Inserimento dei 10 interi
    printf("Inserisci 10 interi:\n");
    for (int i = 0; i < ARRAY_SIZE; i++) {
        printf("[%d]: ", i + 1);

        // Controllo dell'input per numeri validi
        while (scanf("%d", &vector[i]) != 1) {
            printf("Input non valido. Inserisci un numero intero: ");
            while (getchar() != '\n'); // Pulisce il buffer
        }
    }

    // Visualizzazione del vettore inserito
    printf("\nIl vettore inserito è:\n");
    for (int i = 0; i < ARRAY_SIZE; i++) {
        printf("[%d]: %d\n", i + 1, vector[i]);
    }

    // Ordinamento del vettore (bubble sort)
    for (int j = 0; j < ARRAY_SIZE - 1; j++) {
        for (int k = 0; k < ARRAY_SIZE - j - 1; k++) {
            if (vector[k] > vector[k + 1]) {
                int temp = vector[k];
                vector[k] = vector[k + 1];
                vector[k + 1] = temp;
            }
        }
    }

    // Visualizzazione del vettore ordinato
    printf("\nIl vettore ordinato è:\n");
    for (int i = 0; i < ARRAY_SIZE; i++) {
        printf("[%d]: %d\n", i + 1, vector[i]);
    }

    // Tentativo di accedere a un indice non valido (solo in modalità 2)
    if (scelta == 2) {
        printf("\n-----------------------------------------\n");
        printf("MODALITÀ ERRORE: Provo ad accedere a un indice non valido...\n");
        printf("Valore letto da un indice non valido: %d\n", vector[ARRAY_SIZE + 1]);
    }

    printf("=========================================\n");
    printf("Programma terminato.\n");
    return 0;
}
