function populacao = geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes)
  % Parâmetros
  qtdePessoasDoTurno = size(funcionariosDoTurno, 1);

  % Inicializa a população
  % Dimensões: [qtdeIndividuos, qtdePessoasDoTurno, qtdeDiasDoMes]
  populacao = zeros(qtdeIndividuos, qtdePessoasDoTurno, qtdeDiasDoMes);

  % Gera a população inicial
  for contIndividuo = 1:qtdeIndividuos
    for contPessoa = 1:qtdePessoasDoTurno
      % Gera escala válida para este funcionário
      do
        individuo = rand(qtdeDiasDoMes, 1) > 0.5;
      until ~validaSolucao(individuo)

      populacao(contIndividuo, contPessoa, :) = individuo;
    endfor
  endfor

endfunction
