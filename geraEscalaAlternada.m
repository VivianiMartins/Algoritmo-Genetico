function individuo = geraEscalaAlternada(individuo, diasDisponiveis, qtdeDiasDoMes, escala, dadosFuncionario)
  %% Gera escala alternada nos dias disponíveis
  %% Regras:
  %%   - Não pode haver 1's consecutivos
  %%   - Total de 1's não pode passar de ceil(qtdeDiasDoMes/2)
  %%   - Preferencialmente alternado

  maxDiasTrabalhados = ceil(qtdeDiasDoMes / 2);
  contDiasTrabalhados = 0;

   if escala == 1
    prev = dadosFuncionario(end);
    for d = diasDisponiveis
      % Verifica se ainda pode alocar mais dias de trabalho
      if contDiasTrabalhados < maxDiasTrabalhados
        if prev == 1
          % Se trabalhou no dia anterior, hoje não pode trabalhar
          individuo(d) = 0;
          prev = 0;
        else
          % Decide trabalhar
          %trabalha = 1;
          % Decide aleatoriamente (50% de chance)
          %trabalha = rand() > 0.5;
          % 70% de chance de ser 1
          trabalha = rand() > 0.3;
          individuo(d) = trabalha;

          if trabalha
            contDiasTrabalhados = contDiasTrabalhados + 1;
            prev = 1;
          else
            prev = 0;
          endif
         endif
      else
         % Já atingiu o limite de dias trabalhados
         break;
      endif
    endfor
   endif


endfunction
