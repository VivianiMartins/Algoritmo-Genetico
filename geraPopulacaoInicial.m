function populacao = geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes)
  % Gera população inicial para algoritmo genético de escalas de trabalho
  %
  % Entrada:
  %   funcionariosDoTurno: matriz com dados dos funcionários [ID, nome, turno, ferias, ...]
  %   qtdeIndividuos: número de indivíduos (soluções) na população
  %   qtdeDiasDoMes: número de dias no mês
  %
  % Saída:
  %   populacao: matriz 3D [qtdeIndividuos x qtdeFuncionarios x qtdeDiasDoMes]
  %              Cada fatia populacao(i,:,:) é um indivíduo (escala completa)
  %              Linhas: funcionários | Colunas: dias do mês
  %              Valores: 0 (não trabalha) ou 1 (trabalha)

  % Parâmetros
  qtdePessoasDoTurno = size(funcionariosDoTurno, 1);

  % Inicializa a população 3D
  % Dimensões: [indivíduos, funcionários, dias]
  populacao = zeros(qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos);

  fprintf('Gerando população inicial...\n');
  fprintf('Indivíduos: %d | Funcionários: %d | Dias: %d\n', ...
           qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos);

  % Gera cada indivíduo da população
  for contIndividuo = 1:qtdeIndividuos

    % Para cada funcionário neste indivíduo
    for contPessoa = 1:qtdePessoasDoTurno

      % Verifica se o funcionário está de férias
      estaDeFerias = funcionariosDoTurno(contPessoa, 4);  % Coluna 4: férias

      % Se estiver de férias, deixa todos os dias zerados (não trabalha)
      if estaDeFerias == 1
        individuo = zeros(1, qtdeDiasDoMes);  % Já está zerado por padrão
      else
        % Gera escala válida para este funcionário


        prev = 0;
        for d = 1:qtdeDiasDoMes
          if prev == 1
            % se trabalhou no dia anterior, hoje não pode trabalhar
            individuo(d) = 0;
            prev = 0;
          else
            % caso contrário, decide aleatoriamente (ajuste probabilidade se quiser)
            individuo(d) = rand() > 0.5;
            prev = individuo(d);
          endif
        endfor
      endif


      % Armazena a escala deste funcionário neste indivíduo
      populacao( contPessoa, :, contIndividuo) = individuo;

    endfor

    % Feedback de progresso a cada 10% dos indivíduos
    if mod(contIndividuo, max(1, floor(qtdeIndividuos/10))) == 0
      fprintf('Progresso: %d/%d indivíduos gerados (%.1f%%)\n', ...
              contIndividuo, qtdeIndividuos, (contIndividuo/qtdeIndividuos)*100);
    endif

  endfor

  fprintf('População gerada com sucesso!\n');
  fprintf('Dimensões da população: %s\n', mat2str(size(populacao)));
endfunction
