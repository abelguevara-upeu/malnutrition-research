/**
 * Crea en Google Forms la ficha de validación TAM2 (19 ítems) y la hoja
 * de cálculo que recibe las respuestas.
 *
 * Uso: script.google.com > Nuevo proyecto > pegar este archivo >
 * seleccionar crearFicha > Ejecutar > autorizar. Los enlaces salen en
 * el registro de ejecución.
 *
 * Fuente de los ítems: docs/docs/instrumento_validacion_tam.md
 */

const TITULO = 'Ficha de validación por juicio de expertos';

const DESCRIPCION = [
  'Sistema evaluado: Modelo Predictivo de Riesgo de Desnutrición Crónica Infantil en el Perú mediante Machine Learning.',
  '',
  'Universidad Peruana Unión, EP Ingeniería de Sistemas. Investigación V (2026-II), docente Mg. Nemias Saboya Rios.',
  'Equipo: Abel Guevara Huasco, Verónica Vergara Rojas, Pamela Vallejos Cotrina.',
  '',
  'Esta ficha recoge su valoración profesional sobre el sistema que acaba de conocer. Se basa en el Modelo de ' +
    'Aceptación Tecnológica 2 (Venkatesh y Davis, 2000). Sus respuestas se usan solo con fines académicos, de ' +
    'forma agregada y sin identificar individualmente a los participantes. Toma unos 10 minutos.',
].join('\n');

const ESCALA = '1 = Totalmente en desacuerdo · 2 = En desacuerdo · 3 = Ni de acuerdo ni en desacuerdo · ' +
  '4 = De acuerdo · 5 = Totalmente de acuerdo';

const CONSTRUCTOS = [
  ['Relevancia para el trabajo', '¿El sistema se relaciona con las tareas que usted realiza?', [
    ['R1', 'En mi ámbito de trabajo, usar un sistema como este sería importante.'],
    ['R2', 'En mi ámbito de trabajo, usar un sistema como este sería pertinente para decidir intervenciones nutricionales.'],
  ]],
  ['Calidad del resultado', '¿Confía en lo que el sistema entrega?', [
    ['C1', 'Los factores de riesgo que identifica por departamento son coherentes con mi experiencia profesional.'],
    ['C2', 'Confío en que los niveles de riesgo que asigna el sistema son acertados.'],
  ]],
  ['Demostrabilidad del resultado', '¿Se entiende por qué el sistema llega a su resultado?', [
    ['D1', 'Comprendo por qué el sistema asigna un nivel de riesgo a un niño concreto.'],
    ['D2', 'Podría explicar a un colega los resultados que entrega el sistema.'],
  ]],
  ['Utilidad percibida', '¿El sistema mejoraría su trabajo?', [
    ['U1', 'El sistema me permitiría priorizar qué niños atender primero cuando los recursos son limitados.'],
    ['U2', 'Usarlo ahorraría tiempo frente a los métodos actuales de identificación de casos.'],
    ['U3', 'En conjunto, mejoraría la efectividad del trabajo de focalización.'],
  ]],
  ['Facilidad de uso percibida', '¿El sistema resulta sencillo de usar?', [
    ['F1', 'Ingresar los datos de un niño en el sistema es sencillo.'],
    ['F2', 'El nivel de riesgo y el mapa departamental se leen sin dificultad.'],
    ['F3', 'Aprender a usar el sistema no requeriría una capacitación extensa.'],
  ]],
  ['Condiciones para su uso', '¿Existen en su entorno los medios para usarlo?', [
    ['K1', 'Salvo la hemoglobina, los datos que solicita el sistema están disponibles en los registros de mi ámbito de trabajo.'],
    ['K2', 'El dato de hemoglobina suele estar disponible para los niños que atiendo.'],
    ['K3', 'Mi institución cuenta con los medios (equipos, conectividad, personal) para usar una herramienta así.'],
  ]],
  ['Respaldo del entorno profesional', '', [
    ['S1', 'Mis colegas considerarían adecuado el uso de una herramienta como esta.'],
    ['S2', 'Las autoridades de salud de mi ámbito apoyarían su incorporación.'],
  ]],
  ['Intención de uso', '', [
    ['I1', 'Usaría este sistema si estuviera disponible en mi ámbito de trabajo.'],
    ['I2', 'Recomendaría su uso a colegas del área de nutrición o salud pública.'],
  ]],
];

const ABIERTAS = [
  '¿Qué variables o información adicional debería incorporar el sistema?',
  '¿Qué limitaciones identifica desde su experiencia profesional?',
  '¿En qué escenario concreto de su práctica aplicaría esta herramienta?',
  'Recomendaciones para una siguiente versión',
];

function crearFicha() {
  const form = FormApp.create(TITULO)
    .setDescription(DESCRIPCION)
    .setProgressBar(true)
    .setCollectEmail(false)
    .setAllowResponseEdits(false)
    .setShowLinkToRespondAgain(false)
    .setConfirmationMessage('Gracias por su evaluación. Sus respuestas fueron registradas.');

  form.addSectionHeaderItem().setTitle('I. Datos del evaluador');
  form.addTextItem().setTitle('Nombres y apellidos').setRequired(true);
  form.addMultipleChoiceItem().setTitle('Profesión')
    .setChoiceValues(['Nutricionista', 'Médico', 'Enfermero/a'])
    .showOtherOption(true).setRequired(true);
  form.addMultipleChoiceItem().setTitle('Grado académico')
    .setChoiceValues(['Maestría', 'Doctorado'])
    .showOtherOption(true).setRequired(true);
  form.addTextItem().setTitle('Años de experiencia en el área asistencial')
    .setValidation(FormApp.createTextValidation().requireWholeNumber().build())
    .setRequired(true);
  form.addTextItem().setTitle('Institución donde labora');
  form.addMultipleChoiceItem().setTitle('Región de desempeño')
    .setChoiceValues(['Costa', 'Sierra', 'Selva']);
  form.addTextItem().setTitle('Correo electrónico')
    .setValidation(FormApp.createTextValidation().requireTextIsEmail().build());

  CONSTRUCTOS.forEach(([nombre, pregunta, items], i) => {
    const seccion = form.addPageBreakItem().setTitle(`${toRoman(i + 3)}. ${nombre}`);
    seccion.setHelpText([pregunta, ESCALA].filter(Boolean).join('\n\n'));
    items.forEach(([codigo, texto]) => {
      form.addScaleItem()
        .setTitle(`${codigo}. ${texto}`)
        .setBounds(1, 5)
        .setLabels('Totalmente en desacuerdo', 'Totalmente de acuerdo')
        .setRequired(true);
    });
  });

  form.addPageBreakItem().setTitle('XI. Valoración global');
  form.addScaleItem()
    .setTitle('Del 1 al 10, ¿qué potencial le asigna a esta herramienta para el trabajo en salud pública?')
    .setBounds(1, 10)
    .setLabels('Ninguno', 'Muy alto')
    .setRequired(true);

  form.addPageBreakItem().setTitle('XII. Preguntas abiertas');
  ABIERTAS.forEach(q => form.addParagraphTextItem().setTitle(q));

  const hoja = SpreadsheetApp.create(`${TITULO} (respuestas)`);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, hoja.getId());

  Logger.log('Enlace para los expertos: ' + form.getPublishedUrl());
  Logger.log('Editar el formulario:     ' + form.getEditUrl());
  Logger.log('Hoja de respuestas:       ' + hoja.getUrl());
}

function toRoman(n) {
  return ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'][n];
}
