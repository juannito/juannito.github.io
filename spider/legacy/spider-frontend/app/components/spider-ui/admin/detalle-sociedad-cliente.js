import Component from '@ember/component';
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import { observer } from "@ember/object";

export default Component.extend({
  tagName: "",
  store: service(),
  perfil_: service("perfil"),
  perfil: null,
  sociedad: null,
  dropdown: false,

  onSociedadChange: observer("sociedadId", function() {
    this.set("dropdown", false);
    this.traerPropiedades.perform();
    this.traerProyectos.perform();
    this.traerParticipaciones.perform();
  }),

  didInsertElement() {
    this._super(...arguments);
    if (this.perfilId) {
      this.traerSociedades.perform();
    }
    this.traerParticipaciones.perform();
    this.traerPropiedades.perform();
    this.traerProyectos.perform();
  },

  traerSociedades: task(function*() {
      let sociedades =  yield this.store.query("sociedad", {
        perfil_id: this.perfilId,
        soloMisSociedades: true,
        noCrowdfunding: true
      });
      return sociedades;
  }),

  traerParticipaciones: task(function*() {
      let participaciones =  yield this.store.query("participacion", {
        sociedad_id: this.sociedadId,
      });
      return participaciones;
  }),

  traerPropiedades: task(function*() {
    let fields = [
      "id",
      "nombre",
      "direccion",
      "vacante",
      "documento_presale_url",
      "documento_deed_url",
      "documento_lease_url",
      "documento_insurance_url",
      "documento_insurance",
      "documento_presale",
      "documento_deed",
      "documento_lease",
      "documento_invoice",
    ];
    let query = {
      sociedad_id: this.sociedadId,
      fields: fields,
      incluir_agrupadas: true,
      "page[size]": 9999,
    };
    if (this.perfilId !== undefined) {
      query.misPropiedades = true;
      query.perfil_id = this.perfilId;
    }

    let propiedades = yield this.store.query("propiedad", query);
    return propiedades;
  }),

  traerProyectos: task(function*() {
    let query = {
      sociedad_id: this.sociedadId,
      crowdfunding: false,
    };
    if (this.perfilId !== undefined) {
      query.perfil_id = this.perfilId;
      query.misProyectos = true;
    }

    let proyectos = yield this.store.query("proyecto", query);
    return proyectos;
  }),

  actions: {
    toggleDropdown() {
      this.toggleProperty("dropdown");
    }
  }
});
