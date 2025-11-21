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
  [funcDiurnos, funcNoturnos, numDiasMes] = transformarListaFuncionarios(listaFuncionarios);
  tempoDecorrido = toc(tempoInicio);

  fprintf('\n========== RELATÓRIO DE FUNCIONÁRIOS ==========\n');
  fprintf('Total de funcionários: %d\n', size(listaFuncionarios, 1));
  fprintf('Funcionários diurnos: %d\n', size(funcDiurnos, 1));
  fprintf('Funcionários noturnos: %d\n', size(funcNoturnos, 1));
  fprintf('==============================================\n\n');

  %%%% Parâmetros %%%%
  qtdeIndividuos = 5;

  % Gerando as populações iniciais de cada turno separadamente:
  populacaoDiurna = geraPopulacaoInicial(funcDiurnos, qtdeIndividuos, numDiasMes);

  % Pega o indivíduo 5 completo (toda a escala)
  individuo5 = populacaoDiurna(5, :, :);  % matriz [funcionários x dias]

  % Pega a escala do funcionário de férias no individuo 6
  escalaFunc14 = populacaoDiurna(5, 14, :);  % vetor [1 x dias]

  % RESULTADO
  keyboard
  tempoTotal = toc(tempoInicio); % Tempo total de execução
  fprintf('Dimensões da população: %d x %d x %d\n', size(populacaoDiurna, 1), size(populacaoDiurna, 2), size(populacaoDiurna, 3));
  fprintf('Tempo Total: %.2f segundos (%.2f minutos)\n', tempoTotal, tempoTotal/60);
  %populacaoNoturna = geraPopulacaoInicial(funcNoturnos, qtdeIndividuos, numDiasMes);

end

