function [funcionariosDiurnos, funcionariosNoturnos] = transformarListaFuncionarios(listaFuncionarios)
  % Transforma a lista de funcionários em matrizes separadas por turno
  % ESTRUTURA DO CSV (SEM CABEÇALHO):
  % Coluna 1: Nome
  % Coluna 2: Cargo
  % Coluna 3: Turno
  % Coluna 4: Férias
  % Coluna 5: Reescal
  % Coluna 6: Dias (quantidade de dias para reescala-que o funcionario esta de atestado/licensa)
  % Colunas 7-36: Dias do mês (1-30)
  %
  % ESTRUTURA DA MATRIZ DE SAÍDA:
  % Coluna 1: ID do funcionário (linha original no CSV)
  % Coluna 2: Cargo (1=Farmacêutico, 2=Auxiliar)
  % Coluna 3: Turno (1=Diurno, 2=Noturno)
  % Coluna 4: Férias (0=Não, 1=Sim)
  % Coluna 5: Reescal (0=Não, 1=Sim)
  % Coluna 6: Quantidade de dias para reescala
  % Colunas 7-36: Dias do mês (marcação de trabalho 0 ou 1)

  % Inicializa contadores
  contDiurnos = 0;
  contNoturnos = 0;

  % Obtém número de linhas e colunas
  numLinhas = size(listaFuncionarios, 1);
  numColunas = size(listaFuncionarios, 2);

  % Número de funcionários
  numFuncionarios = numLinhas;

  % Calcula quantos dias do mês existem no arquivo (total de colunas - 5 colunas fixas)
  numDiasMes = numColunas - 5;  % 35 - 5 = 30 dias
  numColunasMatriz = 6 + numDiasMes;  % Tamanho da matriz de saída (6 dados + 30 dias)

  % Cria matrizes temporárias para armazenar dados de cada turno
  matrizTemp_Diurnos = zeros(numFuncionarios, numColunasMatriz);
  matrizTemp_Noturnos = zeros(numFuncionarios, numColunasMatriz);

  % Percorre cada funcionário
  for cont = 1:numLinhas

    % Cargo: 1 para farmacêutico, 2 para auxiliar
    cargo = lower(strtrim(listaFuncionarios{cont, 2}));
    if strcmp(cargo, "farmacêutico") || strcmp(cargo, "farmaceutico")
      cargoNumerico = 1;
    else
      cargoNumerico = 2;
    endif

    % Turno: 1 para diurno, 2 para noturno
    turno = lower(strtrim(listaFuncionarios{cont, 3}));

    % Férias: 0 ou 1
    ferias = lower(strtrim(listaFuncionarios{cont, 4}));
    if strcmp(ferias, "sim") || strcmp(ferias, "1")
      feriasNumerico = 1;
    else
      feriasNumerico = 0;
    endif

    % Reescal: 0 ou 1
    reescal = lower(strtrim(listaFuncionarios{cont, 5}));
    if strcmp(reescal, "sim") || strcmp(reescal, "1")
      reescalNumerico = 1;
    else
      reescalNumerico = 0;
    endif

    % Quantidade de dias para reescala (coluna 5)
    qtdeDiasReescala = listaFuncionarios{cont, 6};
    if !isnumeric(qtdeDiasReescala)
      qtdeDiasReescala = str2num(strtrim(qtdeDiasReescala));
    endif

    % Converte os dias do mês (colunas 7 em diante) para numérico
    diasDoMes = zeros(1, numDiasMes);
    for d = 1:numDiasMes
      valor = listaFuncionarios{cont, 5 + d};
      if isnumeric(valor)
        diasDoMes(d) = valor;
      else
        diasDoMes(d) = str2num(strtrim(valor));
      endif
    endfor

    % Armazena dados na matriz correta de acordo com o turno
    if strcmp(turno, "diurno")
      contDiurnos = contDiurnos + 1;
      matrizTemp_Diurnos(contDiurnos, 1) = cont;                  % ID
      matrizTemp_Diurnos(contDiurnos, 2) = cargoNumerico;         % Cargo
      matrizTemp_Diurnos(contDiurnos, 3) = 1;                     % Turno diurno
      matrizTemp_Diurnos(contDiurnos, 4) = feriasNumerico;        % Férias
      matrizTemp_Diurnos(contDiurnos, 5) = reescalNumerico;       % Reescal
      matrizTemp_Diurnos(contDiurnos, 6) = qtdeDiasReescala;      % Qtde dias reescala
      matrizTemp_Diurnos(contDiurnos, 7:end) = diasDoMes;         % Dias do mês
    else
      contNoturnos = contNoturnos + 1;
      matrizTemp_Noturnos(contNoturnos, 1) = cont;                % ID
      matrizTemp_Noturnos(contNoturnos, 2) = cargoNumerico;       % Cargo
      matrizTemp_Noturnos(contNoturnos, 3) = 2;                   % Turno noturno
      matrizTemp_Noturnos(contNoturnos, 4) = feriasNumerico;      % Férias
      matrizTemp_Noturnos(contNoturnos, 5) = reescalNumerico;     % Reescal
      matrizTemp_Noturnos(contNoturnos, 6) = qtdeDiasReescala;    % Qtde dias reescala
      matrizTemp_Noturnos(contNoturnos, 7:end) = diasDoMes;       % Dias do mês
    endif
  endfor

  % Remove linhas vazias (zeros) das matrizes
  funcionariosDiurnos = matrizTemp_Diurnos(1:contDiurnos, :);
  funcionariosNoturnos = matrizTemp_Noturnos(1:contNoturnos, :);

endfunction
