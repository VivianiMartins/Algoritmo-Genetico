function funcaoPrincipal_AG()
##  qtdeEquipes = 2;
  qtdePessoasPorEquipe = 20;
  qtdeIndividuos = 50;
  qtdeDiasDoMes = 30;
  qtdeTurnosPorDia = 2;
  populacao = geraPopulacaoInicial(qtdePessoasPorEquipe, qtdeIndividuos, qtdeDiasDoMes, qtdeTurnosPorDia);
end

function populacao = geraPopulacaoInicial(qtdePessoasPorEquipe, qtdeIndividuos, qtdeDiasDoMes, qtdeTurnosPorDia)
  populacao = zeros(qtdeIndividuos, qtdePessoasPorEquipe, qtdeDiasDoMes, qtdeTurnosPorDia);

  for contIndividuo = 1:qtdeIndividuos
    for contPessoa = 1:qtdePessoasPorEquipe
      turnoDeTrabalho = 1; %% aqui vem um getTurnoPessoa
      do
        temp = zeros(qtdeDiasDoMes, qtdeTurnosPorDia);
        temp(:, turnoDeTrabalho) = rand(qtdeDiasDoMes, 1) > 0.5;
      until ~validaSolucao(temp, 1)
      populacao(contIndividuo, contPessoa, :, :) = temp;
    endfor
  endfor
end

