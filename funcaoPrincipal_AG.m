function funcaoPrincipal_AG()
  pkg load io

  % importando a tabela com os funcionários contendo: nome, cargo, turno e férias.
  listaFuncionarios = csv2cell('listaFuncionarios.csv');
  listaFuncionarios = listaFuncionarios(2:end,:,:,:);

  % terei duas matrizes de funcionarios por turno:
  [funcDiurnos, funcNoturnos] = transformarListaFuncionarios(listaFuncionarios);

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
  fprintf('Dimensões da população: %d x %d x %d\n', size(populacaoDiurna, 1), size(populacaoDiurna, 2), size(populacaoDiurna, 3));

  %populacaoNoturna = geraPopulacaoInicial(funcNoturnos, qtdeIndividuos, qtdeDiasDoMes);

end

