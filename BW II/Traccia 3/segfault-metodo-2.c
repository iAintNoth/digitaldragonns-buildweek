#include <stdio.h>

int main() {
    int vector[10], i, j, k;
    int swap_var;
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
    for (i = 0; i < 10; i++) {
        int c = i + 1;
        printf("[%d]: ", c);

        // Controllo dell'input per numeri validi
        while (scanf("%d", &vector[i]) != 1) {
            printf("Input non valido. Inserisci un numero intero: ");
            while (getchar() != '\n'); // Pulisce il buffer
        }
    }

    // Visualizzazione del vettore inserito
    printf("\nIl vettore inserito e':\n");
    for (i = 0; i < 10; i++) {
        int t = i + 1;
        printf("[%d]: %d\n", t, vector[i]);
    }

    // Ordinamento del vettore (bubble sort)
    for (j = 0; j < 10 - 1; j++) {
        for (k = 0; k < 10 - j - 1; k++) {
            if (vector[k] > vector[k + 1]) {
                swap_var = vector[k];
                vector[k] = vector[k + 1];
                vector[k + 1] = swap_var;
            }
        }
    }

    // Tentativo di accedere a memoria non valida (solo in modalità 2)
    if (scelta == 2) {
        printf("\n-----------------------------------------\n");
        printf("MODALITÀ ERRORE: Provo ad accedere a memoria non valida...\n");
        int *ptr = (int *)0xDEADBEEF; // Puntatore a una posizione non valida
        printf("Valore letto dalla memoria non valida: %d\n", *ptr);
    }

    // Visualizzazione del vettore ordinato
    printf("\nIl vettore ordinato e':\n");
    for (j = 0; j < 10; j++) {
        int g = j + 1;
        printf("[%d]: %d\n", g, vector[j]);
    }

    printf("=========================================\n");
    printf("Programma terminato.\n");
    return 0;
}
