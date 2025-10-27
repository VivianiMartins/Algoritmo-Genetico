function funcaoPrincipal_AG()
  pkg load io

  % ============================================================
  % INICIAR CONTADOR DE TEMPO
  % ============================================================
  tempoInicio = tic; % Inicia cronômetro

  % importando a tabela com os funcionários contendo: nome, cargo, turno e férias.
  listaFuncionarios = csv2cell('listaFuncionarios.csv');
  listaFuncionarios = listaFuncionarios(2:end,:,:,:);

  % terei duas matrizes de funcionarios por turno:
  [funcDiurnos, funcNoturnos] = transformarListaFuncionarios(listaFuncionarios);
  tempoDecorrido = toc(tempoInicio);

  fprintf('\n========== RELATÓRIO DE FUNCIONÁRIOS ==========\n');
  fprintf('Total de funcionários: %d\n', size(listaFuncionarios, 1));
  fprintf('Funcionários diurnos: %d\n', size(funcDiurnos, 1));
  fprintf('Funcionários noturnos: %d\n', size(funcNoturnos, 1));
  fprintf('==============================================\n\n');

  %%%% Parâmetros %%%%
  qtdeIndividuos = 50;
  % dias do mês da escala, 28,30 ou 31
  qtdeDiasDoMes = 30;

  % Gerando as populações iniciais de cada turno separadamente:
  populacaoDiurna = geraPopulacaoInicial(funcDiurnos, qtdeIndividuos, qtdeDiasDoMes);
  % RESULTADO
  tempoTotal = toc(tempoInicio); % Tempo total de execução
  fprintf('Dimensões da população: %d x %d x %d\n', size(populacaoDiurna, 1), size(populacaoDiurna, 2), size(populacaoDiurna, 3));
  fprintf('Tempo Total: %.2f segundos (%.2f minutos)\n', tempoTotal, tempoTotal/60);
  %populacaoNoturna = geraPopulacaoInicial(funcNoturnos, qtdeIndividuos, qtdeDiasDoMes);

end

