function populacao = geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes)
  % Parâmetros
  qtdePessoasDoTurno = size(funcionariosDoTurno, 1);

  % Inicializa a população
  % Dimensões: [qtdeIndividuos, qtdePessoasDoTurno, qtdeDiasDoMes + 1]
  % Coluna 1: ID do funcionário | Colunas 2 até end: dias trabalhados

  populacao = zeros(qtdeIndividuos, qtdePessoasDoTurno, qtdeDiasDoMes + 1);

  % Gera a população inicial
  for contIndividuo = 1:qtdeIndividuos
    % Para cada indivíduo, embaralha os IDs disponíveis (sem repetição)
    idsDisponiveis = funcionariosDoTurno(:, 1);  % Pega todos os IDs
    idsEmbaralhados = idsDisponiveis(randperm(length(idsDisponiveis)));

    for contPessoa = 1:qtdePessoasDoTurno
      % Atribui um ID único (sem repetição) para este funcionário neste indivíduo
      idFuncionario = idsEmbaralhados(contPessoa);
      populacao(contIndividuo, contPessoa, 1) = idFuncionario;

      % Busca os dados do funcionário na matriz original
      indiceFuncionario = find(funcionariosDoTurno(:, 1) == idFuncionario);
      estaDeFerias = funcionariosDoTurno(indiceFuncionario, 4);

      % Se estiver de férias, não aloca dias de trabalho
      if estaDeFerias == 1
        continue;
      endif

      % Gera escala válida para este funcionário
      do
        individuo = rand(qtdeDiasDoMes, 1) > 0.5;
      until validaSolucao(individuo)

      % Armazena a escala (dias 2 até qtdeDiasDoMes+1)
      populacao(contIndividuo, contPessoa, 2:end) = individuo;
    endfor
  endfor

  fprintf('População gerada com sucesso!\n');
  fprintf('Indivíduos: %d | Funcionários: %d | Dias: %d (+ ID)\n', qtdeIndividuos, qtdePessoasDoTurno, qtdeDiasDoMes);

endfunction
