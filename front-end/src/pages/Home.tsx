import { useState, useEffect } from 'react';
import { TrendingDown, Leaf, Loader } from 'lucide-react';
import { graphQLClient, queries } from '../services/graphql';

interface State {
  uf: string;
  name: string;
  baseTariffKwh: number;
}

interface Supplier {
  supplierId: number;
  supplierName: string;
  logoUrl?: string;
  solutionType: string;
  costKwh: number;
  baseCost: number;
  supplierCost: number;
  economy: number;
  economyPercentage: number;
  totalCustomers: number;
  averageRating: number;
}

interface SolutionAvailability {
  solutionType: string;
  suppliers: Supplier[];
  bestEconomy: number;
  bestSupplier: string;
}

interface SimulationResult {
  stateUf: string;
  consumptionKwh: number;
  baseCost: number;
  solutions: SolutionAvailability[];
}

export default function Home() {
  const [states, setStates] = useState<State[]>([]);
  const [estado, setEstado] = useState('SP');
  const [consumo, setConsumo] = useState(5000);
  const [resultados, setResultados] = useState<SimulationResult | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [carregandoEstados, setCarregandoEstados] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    const carregarEstados = async () => {
      try {
        setCarregandoEstados(true);
        const data: any = await graphQLClient.request(queries.GET_STATES);
        setStates(data.states);
        if (data.states.length > 0) {
          setEstado(data.states[0].uf);
        }
      } catch (err) {
        console.error('Erro ao carregar estados:', err);
        setErro('Erro ao carregar estados.');
      } finally {
        setCarregandoEstados(false);
      }
    };

    carregarEstados();
  }, []);

  const handleSimular = async () => {
    try {
      setCarregando(true);
      setErro(null);
      const data: any = await graphQLClient.request(queries.SIMULATE, {
        stateUf: estado,
        consumptionKwh: consumo,
      });
      setResultados(data.simulate);
    } catch (err) {
      console.error('Erro na simulação:', err);
      setErro('Erro ao simular. Tente novamente.');
    } finally {
      setCarregando(false);
    }
  };

  const estadoNome = states.find((s) => s.uf === estado)?.name || estado;
  const consumoAtualFormatado = consumo.toLocaleString('pt-BR');

  return (
    <div>
      <header className="padding-10 border-b border-slate-200">
        <div className="flex items-center gap-3 ml-8 pl-4">
            <div className="padding-10 bg-gradient-to-br from-emerald-400 to-blue-500 rounded-lg">
                <Leaf className="w-6 h-6 text-white" />
            </div>
            <div>
                <h1 className="text-2xl font-bold text-slate-900">Clarke Energia</h1>
                <p className="text-xs text-slate-500">Simulador de Economia</p>
            </div>
        </div>
      </header>

      <section>
        <div className="flex flex-col m-8 justify-center dir gap-4">
            <div>
                <h2 className="text-4xl md:text-5xl text-center font-bold text-slate-900 mb-4">
                    Descubra sua economia de energia
                </h2>
            </div>
            <div>
                <p className="text-lg text-center text-slate-600 mx-auto">
                    Simule quanto sua empresa pode economizar adotando soluções de energia renovável
                </p>
            </div>
        </div>

        {erro && (
          <div className="bg-red-50 border border-red-300 rounded-2xl p-4 mb-8 text-red-800">
            {erro}
          </div>
        )}

        <div className="bg-white rounded-2xl shadow-xl p-8 md:p-10 mb-12">
          <div className="flex flex-col md:flex-row gap-8 justify-center">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Selecione seu Estado (pode demorar a aparecer por conta do serviço de cloud gratuito)
              </label>
              <select
                value={estado}
                onChange={(e) => setEstado(e.target.value)}
                disabled={carregandoEstados}
                className="min-w-64 px-4 py-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-slate-900 font-medium transition disabled:opacity-50"
              >
                {states.map((est) => (
                  <option key={est.uf} value={est.uf}>
                    {est.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                Consumo Mensal (kWh)
              </label>
              <div className="relative">
                <input
                  type="number"
                  value={consumo}
                  onChange={(e) => setConsumo(Number(e.target.value))}
                  className="min-w-64 px-4 py-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-slate-900 font-medium transition"
                  min="100"
                  step="100"
                />
                <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-500 font-medium">
                  kWh
                </span>
              </div>
            </div>
          </div>

          <div className="flex justify-center">
                <button 
                    onClick={handleSimular}
                    disabled={carregando || carregandoEstados}
                    className="min-w-128 mt-8 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg transition cursor-pointer">
                        {carregando ? (
                    <>
                        <Loader className="w-5 h-5 animate-spin" />
                    </>
                    ) : (
                    <>
                        Simular Economia
                    </>
                    )}
                </button>
          </div>
        </div>

        {resultados && !carregando && (
          <div className="flex flex-col gap-8 mb-12 justify-center">
            <div className="bg-gradient-to-r from-emerald-50 to-blue-50 rounded-2xl p-8 border border-emerald-200 max-w-4xl mx-auto">
              <div className="flex items-center gap-3 mb-2">
                <TrendingDown className="w-6 h-6 text-emerald-600" />
                <h3 className="text-xl font-bold text-slate-900">Seus Resultados</h3>
              </div>
              <p className="text-slate-600">
                Estado: <span className="font-semibold text-slate-900">{estadoNome}</span> • 
                Consumo: <span className="font-semibold text-slate-900">{consumoAtualFormatado} kWh/mês</span> •
                Custo Base: <span className="font-semibold text-slate-900">R$ {resultados.baseCost.toFixed(2)}</span>
              </p>
            </div>

            {resultados.solutions.length === 0 ? (
              <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-8 text-center text-yellow-800">
                Nenhuma solução disponível para este estado.
              </div>
            ) : (
                <div>{
                    resultados.solutions.map((solution) => (
                        <div className="flex flex-col gap-6 mb-12" key={solution.solutionType}>
                            <div className="text-center">
                                <span style={{fontWeight: 'bold', fontSize: 22}}>{solution.solutionType}</span>
                            </div>
                            <div className="flex gap-6 flex-wrap justify-center">
                                {solution.suppliers.map((supplier) => {
                                const economiaAnual = supplier.economy * 12;
                                return (
                                    <a
                                    target='blank'
                                    href='https://www.clarke.com.br'
                                    key={supplier.supplierId}
                                    className="min-w-128 bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition duration-300 border border-emerald-500 hover:border-blue-300 cursor-pointer"
                                    >
                                    <div className="mb-4">
                                        <h4 className="text-lg font-bold text-slate-900">
                                        {supplier.supplierName}
                                        </h4>
                                        <div className="flex items-center gap-1 mt-2">
                                        <span className="text-yellow-500">★</span>
                                        <span className="text-sm font-semibold text-slate-700">
                                            {supplier.averageRating.toFixed(1)}
                                        </span>
                                        <span className="text-xs text-slate-500">
                                            ({supplier.totalCustomers.toLocaleString('pt-BR')} clientes)
                                        </span>
                                        </div>
                                    </div>

                                    <div className="space-y-3">
                                        <div className="bg-gradient-to-r from-emerald-50 to-blue-50 rounded-lg p-3">
                                        <p className="text-xs text-slate-600 mb-1">Custo por kWh</p>
                                        <p className="text-2xl font-bold text-blue-600">
                                            R$ {supplier.costKwh.toFixed(2)}
                                        </p>
                                        </div>

                                        <div className="space-y-2">
                                        <div className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                                            <span className="text-xs font-medium text-slate-600">Economia/mês</span>
                                            <span className="text-lg font-bold text-emerald-600">
                                            R$ {supplier.economy.toFixed(2)}
                                            </span>
                                        </div>

                                        <div className="flex justify-between items-center p-3 bg-emerald-50 rounded-lg border border-emerald-200">
                                            <span className="text-xs font-medium text-slate-600">Economia/ano</span>
                                            <span className="text-lg font-bold text-emerald-600">
                                            R$ {economiaAnual.toFixed(2)}
                                            </span>
                                        </div>

                                        <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                                            <span className="text-xs font-medium text-slate-600">Redução</span>
                                            <span className="text-lg font-bold text-blue-600">
                                            {supplier.economyPercentage.toFixed(1)}%
                                            </span>
                                        </div>
                                        </div>
                                    </div>
                                    </a>
                                );
                                })}
                            </div>
                        </div>
                    ))
                }</div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
