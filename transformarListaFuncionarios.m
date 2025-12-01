function [funcionariosDiurnos, funcionariosNoturnos, numDiasMes] = transformarListaFuncionarios(listaFuncionarios)
  % Transforma a lista de funcionários em matrizes separadas por turno
  % ESTRUTURA DO CSV (SEM CABEÇALHO):
  % Coluna 1: Nome
  % Coluna 2: Cargo
  % Coluna 3: Turno
  % Coluna 4: Inicio (numérico)
  % Coluna 5: Fim (numérico)
  % Colunas 6-35: Dias do mês (1-30)
  %
  % ESTRUTURA DA MATRIZ DE SAÍDA:
  % Coluna 1: Cargo (1=Farmacêutico, 2=Auxiliar)
  % Coluna 2: Turno (1=Diurno, 2=Noturno)
  % Coluna 3: Inicio (0 se não existir)
  % Coluna 4: Fim (0 se não existir)
  % Colunas 5-34: Dias do mês (marcação de trabalho 0 ou 1)

  % Inicializa contadores
  contDiurnos = 0;
  contNoturnos = 0;

  % Obtém número de linhas e colunas
  numLinhas = size(listaFuncionarios, 1);
  numColunas = size(listaFuncionarios, 2);

  % Número de funcionários
  numFuncionarios = numLinhas;

  % Calcula quantos dias do mês existem no arquivo (total de colunas - 5 colunas fixas)
  numDiasMes = numColunas - 5;  % Total - 5 = dias do mês
  numColunasMatriz = 4 + numDiasMes;  % Tamanho da matriz de saída (4 dados + dias)

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

    % Inicio (coluna 4)
    inicio = listaFuncionarios{cont, 4};
    if !isnumeric(inicio)
      inicio = str2num(strtrim(inicio));
      if isempty(inicio)
        inicio = 0;
      endif
    endif

    % Fim (coluna 5)
    fim = listaFuncionarios{cont, 5};
    if !isnumeric(fim)
      fim = str2num(strtrim(fim));
      if isempty(fim)
        fim = 0;
      endif
    endif

    % Converte os dias do mês (colunas 6 em diante) para numérico
    diasDoMes = zeros(1, numDiasMes);
    for d = 1:numDiasMes
      valor = listaFuncionarios{cont, 5 + d};
      if isnumeric(valor)
        diasDoMes(d) = valor;
      else
        valorConvertido = str2num(strtrim(valor));
        if !isempty(valorConvertido)
          diasDoMes(d) = valorConvertido;
        else
          diasDoMes(d) = 0;
        endif
      endif
    endfor

    % Armazena dados na matriz correta de acordo com o turno
    if strcmp(turno, "diurno")
      contDiurnos = contDiurnos + 1;
      matrizTemp_Diurnos(contDiurnos, 1) = cargoNumerico;         % Cargo
      matrizTemp_Diurnos(contDiurnos, 2) = 1;                     % Turno diurno
      matrizTemp_Diurnos(contDiurnos, 3) = inicio;                % Inicio
      matrizTemp_Diurnos(contDiurnos, 4) = fim;                   % Fim
      matrizTemp_Diurnos(contDiurnos, 5:end) = diasDoMes;         % Dias do mês
    else
      contNoturnos = contNoturnos + 1;
      matrizTemp_Noturnos(contNoturnos, 1) = cargoNumerico;       % Cargo
      matrizTemp_Noturnos(contNoturnos, 2) = 2;                   % Turno noturno
      matrizTemp_Noturnos(contNoturnos, 3) = inicio;              % Inicio
      matrizTemp_Noturnos(contNoturnos, 4) = fim;                 % Fim
      matrizTemp_Noturnos(contNoturnos, 5:end) = diasDoMes;       % Dias do mês
    endif
  endfor

  % Remove linhas vazias (zeros) das matrizes
  funcionariosDiurnos = matrizTemp_Diurnos(1:contDiurnos, :);
  funcionariosNoturnos = matrizTemp_Noturnos(1:contNoturnos, :);

endfunction
