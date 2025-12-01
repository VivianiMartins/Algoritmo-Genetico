function populacao = geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes, escala, diaReescala)
  % Gera população inicial para algoritmo genético de escalas de trabalho
  %
  % Entrada:
  %   funcionariosDoTurno: matriz com dados dos funcionários
  %                        [Cargo, Turno, Inicio, Fim, Dia1, Dia2, ..., DiaN]
  %   qtdeIndividuos: número de indivíduos (soluções) na população
  %   qtdeDiasDoMes: número de dias no mês
  %   escala: 1 para escala (gera do zero), 0 para reescala (usa dias existentes)
  %
  % Saída:
  %   populacao: matriz 3D [qtdeFuncionarios x qtdeDiasDoMes x qtdeIndividuos]
  %              Cada fatia populacao(:,:,i) é um indivíduo (escala completa)
  %              Linhas: funcionários | Colunas: dias do mês
  %              Valores: 0 (não trabalha) ou 1 (trabalha)

  % Parâmetros
  qtdePessoasDoTurno = size(funcionariosDoTurno, 1);

  % Inicializa a população 3D
  % Dimensões: [funcionários, dias, indivíduos]
  populacao = zeros(qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos);

  fprintf('Gerando população inicial...\n');
  fprintf('Funcionários: %d | Dias: %d | Indivíduos: %d \n', ...
           qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos);

  % Gera cada indivíduo da população
  for contIndividuo = 1:qtdeIndividuos

    % Para cada funcionário neste indivíduo
    for contPessoa = 1:qtdePessoasDoTurno

      if escala == 1
        % ESCALA: Gera escala inicial vazia (do zero)
        individuo = zeros(1, qtdeDiasDoMes);
      else
        % REESCALA: Usa os dias já existentes do funcionário
        % Os dias estão da posição 5 em diante em funcionariosDoTurno
        individuo = funcionariosDoTurno(contPessoa, 5:end);
      endif

      % Valida e ajusta a solução de acordo com as regras
      individuo = validaSolucao(individuo, funcionariosDoTurno(contPessoa, :), qtdeDiasDoMes, escala);

      % Armazena a escala deste funcionário neste indivíduo
      populacao(contPessoa, :, contIndividuo) = individuo;

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
