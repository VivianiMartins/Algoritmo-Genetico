function individuo = geraEscalaAlternada(individuo, diasDisponiveis, qtdeDiasDoMes, escala)
  %% Gera escala alternada nos dias disponíveis
  %% Regras:
  %%   - Não pode haver 1's consecutivos
  %%   - Total de 1's não pode passar de ceil(qtdeDiasDoMes/2)
  %%   - Preferencialmente alternado

  maxDiasTrabalhados = ceil(qtdeDiasDoMes / 2);
  contDiasTrabalhados = 0;

   keyboard
  prev = 0;
  for d = diasDisponiveis
    if prev == 1
      % Se trabalhou no dia anterior, hoje não pode trabalhar
      individuo(d) = 0;
      prev = 0;
    else
      % Verifica se ainda pode alocar mais dias de trabalho
      if contDiasTrabalhados < maxDiasTrabalhados
        % Decide aleatoriamente (50% de chance)
        trabalha = rand() > 0.5;
        individuo(d) = trabalha;

        if trabalha
          contDiasTrabalhados = contDiasTrabalhados + 1;
          prev = 1;
        else
          prev = 0;
        endif
      else
        % Já atingiu o limite de dias trabalhados
        individuo(d) = 0;
        prev = 0;
      endif
    endif
  endfor

endfunction
