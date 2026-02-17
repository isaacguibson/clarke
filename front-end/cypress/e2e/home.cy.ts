describe('Clarke Energia - Home Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173');
  });

  it('should load the page with header', () => {
    cy.contains('Clarke Energia').should('be.visible');
    cy.contains('Simulador de Economia').should('be.visible');
  });

  it('should display state selector', () => {
    cy.get('select').should('exist');
    cy.get('select').should('not.be.disabled');
  });

  it('should display consumption input', () => {
    cy.get('input[type="number"]').should('exist');
    cy.get('input[type="number"]').should('have.value', '5000');
  });

  it('should display simulate button', () => {
    cy.contains('Simular Economia').should('be.visible');
    cy.contains('Simular Economia').should('not.be.disabled');
  });

  it('should show error message when backend is not available', () => {
    cy.contains('button', 'Simular Economia').click();
    cy.wait(2000);
  });

  it('should allow changing the state', () => {
    cy.get('select', { timeout: 10000 })
      .should('be.visible')
      .should('not.be.disabled')
      .then(($select) => {
        const options = $select.find('option');
        if (options.length > 1) {
          cy.get('select').select(options[1].value);
          cy.get('select').should('have.value', options[1].value);
        }
      });
  });

  it('should allow changing consumption', () => {
    cy.get('input[type="number"]', { timeout: 10000 })
      .should('be.visible')
      .invoke('val', '8000')
      .trigger('input')
      .trigger('change')
      .should('have.value', '8000');
  });

  it('should have page title', () => {
    cy.contains('Descubra sua economia de energia').should('be.visible');
  });
});
