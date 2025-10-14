function flagValidoOuNao = validaSolucao(individuo, turno)
  %% se o turno da pessoa é diurno, faça...
  keyboard
  if turno == 1
    %% verificando se a pessoa não trabalha no turno noturno
    if any(individuo(:, 2) == 1)
      flagValidoOuNao = 0;
      return;
    end
    %% verificando se a pessoa trabalha mais de um dia seguido
    flagTrabalhaDiaAnterior = nan;
    for contDia = 1:length(individuo)
      flagTrabalhaDiaAtual = individuo(contDia);
      if flagTrabalhaDiaAtual == 1 && flagTrabalhaDiaAnterior == 1
        flagValidoOuNao = 0;
        return;
      endif
      flagTrabalhaDiaAnterior = flagTrabalhaDiaAtual;
    endfor
  endif
end
