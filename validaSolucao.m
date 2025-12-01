
function individuoValido = validaSolucao(individuo, dadosFuncionario, qtdeDiasDoMes, escala)
  %% Valida e gera uma escala válida para o funcionário
  %%
  %% Entrada:
  %%   individuo: vetor com a escala atual [1 x dias] (pode estar vazio/zerado ou preenchido)
  %%   dadosFuncionario: vetor com [Cargo, Turno, Inicio, Fim, Dias...]
  %%   qtdeDiasDoMes: número de dias no mês
  %%
  %% Saída:
  %%   individuoValido: vetor [1 x dias] com escala válida

  % Extrai informações do funcionário
  inicio = dadosFuncionario(3);
  fim = dadosFuncionario(4);


  % Valida se inicio e fim estão dentro do intervalo válido
  if inicio > qtdeDiasDoMes
    error('ERRO: Data de inicio (%d) está fora do intervalo de dias do mês (1-%d)!', inicio, qtdeDiasDoMes);
  endif

  if fim > qtdeDiasDoMes
    error('ERRO: Data de fim (%d) está fora do intervalo de dias do mês (1-%d)!', fim, qtdeDiasDoMes);
  endif

  % Inicializa o indivíduo válido
  if ~escala
    % Mantém a escala existente como base
    individuoValido = individuo;
  else
    % Inicia com zeros para escala nova
    individuoValido = zeros(1, qtdeDiasDoMes);
  endif

  % Verifica se há período de ausência (férias/licença)
  if inicio > 0 || fim > 0
    % Há período de ausência - precisa bloquear os dias

    if inicio > fim % Período atravessa a virada do mês
      % Bloqueia do inicio até o último dia do mês
      for d = inicio:qtdeDiasDoMes
        individuoValido(d) = 0;  % Não trabalha
      endfor

      % Dias disponíveis: de 1 até (inicio-1)
      diasDisponiveis = [];
      if inicio > 1
        diasDisponiveis = 1:(inicio-1);
      endif

    else
      % Período normal dentro do mesmo mês (ex: dia 10 ao dia 20)
      % Bloqueia de inicio até fim
      for d = inicio:fim
        individuoValido(d) = 0;  % Não trabalha
      endfor

      % Dias disponíveis: antes do inicio e depois do fim
      diasDisponiveis = [];

      % Adiciona dias antes do inicio (se existirem)
      if inicio > 1
        diasDisponiveis = [diasDisponiveis, 1:(inicio-1)];
      endif

      % Adiciona dias depois do fim (se existirem)
      if fim < qtdeDiasDoMes
        diasDisponiveis = [diasDisponiveis, (fim+1):qtdeDiasDoMes];
      endif
    endif

    % Gera escala alternada apenas nos dias disponíveis
    if !isempty(diasDisponiveis)
      individuoValido = geraEscalaAlternada(individuoValido, diasDisponiveis, qtdeDiasDoMes, escala);
    endif

  else
    % Não há período de ausência - todos os dias estão disponíveis
    diasDisponiveis = 1:qtdeDiasDoMes;
    individuoValido = geraEscalaAlternada(individuoValido, diasDisponiveis, qtdeDiasDoMes,escala);
  endif

endfunction
