function flagValidoOuNao = validaSolucao(individuo)
  %% Valida se a escala do funcionário atende aos critérios
  %% individuo: vetor com 1 (trabalha) ou 0 (não trabalha) para cada dia

  flagValidoOuNao = 1;  % Inicializa como válido

  %% Verifica se não trabalha mais de um dia seguido
  flagTrabalhaDiaAnterior = 0;
  for contDia = 1:length(individuo)
    flagTrabalhaDiaAtual = individuo(contDia);

    if flagTrabalhaDiaAtual == 1 && flagTrabalhaDiaAnterior == 1
      flagValidoOuNao = 0;
      return;
    endif

    flagTrabalhaDiaAnterior = flagTrabalhaDiaAtual;
  endfor

endfunction
