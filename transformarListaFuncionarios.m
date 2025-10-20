function [funcionariosDiurnos, funcionariosNoturnos] = transformarListaFuncionarios(listaFuncionarios)
  % Inicializa contadores
  contDiurnos = 0;
  contNoturnos = 0;

  % Obtém número de linhas (funcionários)
  numFuncionarios = size(listaFuncionarios, 1);

  % Cria matrizes temporárias para armazenar dados de cada turno
  matrizTemp_Diurnos = zeros(numFuncionarios, 4);
  matrizTemp_Noturnos = zeros(numFuncionarios, 4);

  % Percorre cada funcionário
  for cont = 1:numFuncionarios

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

    % Armazena dados na matriz correta de acordo com o turno
    if strcmp(turno, "diurno")
      contDiurnos = contDiurnos + 1;
      matrizTemp_Diurnos(contDiurnos, 1) = cont;
      matrizTemp_Diurnos(contDiurnos, 2) = cargoNumerico;
      matrizTemp_Diurnos(contDiurnos, 3) = 1;  % Turno diurno
      matrizTemp_Diurnos(contDiurnos, 4) = feriasNumerico;
    else
      contNoturnos = contNoturnos + 1;
      matrizTemp_Noturnos(contNoturnos, 1) = cont;
      matrizTemp_Noturnos(contNoturnos, 2) = cargoNumerico;
      matrizTemp_Noturnos(contNoturnos, 3) = 2;  % Turno noturno
      matrizTemp_Noturnos(contNoturnos, 4) = feriasNumerico;
    endif
  endfor

  % Remove linhas vazias (zeros) das matrizes
  funcionariosDiurnos = matrizTemp_Diurnos(1:contDiurnos, :);
  funcionariosNoturnos = matrizTemp_Noturnos(1:contNoturnos, :);

endfunction
