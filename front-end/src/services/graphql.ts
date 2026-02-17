import { request, gql } from 'graphql-request';

const determineAPIUrl = (): string => {
  const isProduction = import.meta.env.PROD;
  const productionUrl = 'https://clarke-w55t.onrender.com/graphql';
  const localUrl = 'http://localhost:8000/graphql';
  
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  return isProduction ? productionUrl : localUrl;
};

const API_URL = determineAPIUrl();

export const graphQLClient = {
  request: (query: string, variables?: Record<string, any>) => {
    return request(API_URL, query, variables);
  },
};

export const queries = {
  GET_STATES: gql`
    query {
      states {
        uf
        name
        baseTariffKwh
      }
    }
  `,

  SIMULATE: gql`
    query Simulate($stateUf: String!, $consumptionKwh: Float!) {
      simulate(stateUf: $stateUf, consumptionKwh: $consumptionKwh) {
        stateUf
        consumptionKwh
        baseCost
        solutions {
          solutionType
          bestEconomy
          bestSupplier
          suppliers {
            supplierId
            supplierName
            logoUrl
            solutionType
            costKwh
            baseCost
            supplierCost
            economy
            economyPercentage
            totalCustomers
            averageRating
          }
        }
      }
    }
  `,
};
