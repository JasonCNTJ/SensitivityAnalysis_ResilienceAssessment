import numpy as np
import torch
import gpytorch
from sklearn.preprocessing import StandardScaler


def GPRmodel(X_predict):
    row, col = X_predict.shape
    # 加载GPR模型
    # 导入数据
    params = np.loadtxt(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\0915params_2475year.txt')
    edpResults = np.loadtxt(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\0915edpResult_2475year.txt')

    params = params[:, (1, 2, 3, 4, 5, 6, 7, 8, 10)]
    edpResults = np.log(edpResults)
    # params_ridr = np.hstack((params, edpResults[:, (0, 1, 2)]))

    # 创建 StandardScaler 实例
    scaler = StandardScaler()
    # 假设 X 是输入特征数据
    # 在训练集上拟合（计算均值和方差），并对数据进行标准化
    nn = 700
    X_train_scaled = scaler.fit_transform(params[:nn])
    # 在测试集上使用相同的标准化器进行标准化
    X_test_scaled = scaler.transform(X_predict)

    num, _ = params.shape
    train_x = torch.from_numpy(X_train_scaled).to(torch.float)

    train_y_pidr1 = torch.from_numpy(edpResults[:nn, 0]).to(torch.float)
    train_y_pidr2 = torch.from_numpy(edpResults[:nn, 1]).to(torch.float)
    train_y_pidr3 = torch.from_numpy(edpResults[:nn, 2]).to(torch.float)
    train_y_pfa1 = torch.from_numpy(edpResults[:nn, 3]).to(torch.float)
    train_y_pfa2 = torch.from_numpy(edpResults[:nn, 4]).to(torch.float)
    train_y_pfa3 = torch.from_numpy(edpResults[:nn, 5]).to(torch.float)
    train_y_pfa4 = torch.from_numpy(edpResults[:nn, 6]).to(torch.float)

    state_dict_pidr1 = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\pidr1_model_state.pth')
    state_dict_pidr2 = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\pidr2_model_state.pth')
    state_dict_pidr3 = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\pidr3_model_state.pth')
    state_dict_pfa1 = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\pfa1_model_state.pth')
    state_dict_pfa2 = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\pfa2_model_state.pth')
    state_dict_pfa3 = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\pfa3_model_state.pth')
    state_dict_pfa4 = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\pfa4_model_state.pth')
    state_dict_ridr = torch.load(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\ridr_model_state.pth')

    # We will use the simplest form of GP model, exact inference
    class ExactGPModel(gpytorch.models.ExactGP):
        def __init__(self, train_x, train_y, likelihood, dims):
            super(ExactGPModel, self).__init__(train_x, train_y, likelihood)
            self.mean_module = gpytorch.means.ConstantMean()
            self.covar_module = gpytorch.kernels.ScaleKernel(gpytorch.kernels.RBFKernel(ard_num_dims=dims))

        def forward(self, x):
            mean_x = self.mean_module(x)
            covar_x = self.covar_module(x)
            return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)

    # initialize likelihood and model
    likelihood_pidr1 = gpytorch.likelihoods.GaussianLikelihood()
    likelihood_pidr2 = gpytorch.likelihoods.GaussianLikelihood()
    likelihood_pidr3 = gpytorch.likelihoods.GaussianLikelihood()
    likelihood_pfa1 = gpytorch.likelihoods.GaussianLikelihood()
    likelihood_pfa2 = gpytorch.likelihoods.GaussianLikelihood()
    likelihood_pfa3 = gpytorch.likelihoods.GaussianLikelihood()
    likelihood_pfa4 = gpytorch.likelihoods.GaussianLikelihood()

    model_pidr1 = ExactGPModel(train_x, train_y_pidr1, likelihood_pidr1, 9)
    model_pidr2 = ExactGPModel(train_x, train_y_pidr2, likelihood_pidr2, 9)
    model_pidr3 = ExactGPModel(train_x, train_y_pidr3, likelihood_pidr3, 9)
    model_pfa1 = ExactGPModel(train_x, train_y_pfa1, likelihood_pfa1, 9)
    model_pfa2 = ExactGPModel(train_x, train_y_pfa2, likelihood_pfa2, 9)
    model_pfa3 = ExactGPModel(train_x, train_y_pfa3, likelihood_pfa3, 9)
    model_pfa4 = ExactGPModel(train_x, train_y_pfa4, likelihood_pfa4, 9)

    model_pidr1.load_state_dict(state_dict_pidr1)
    model_pidr2.load_state_dict(state_dict_pidr2)
    model_pidr3.load_state_dict(state_dict_pidr3)
    model_pfa1.load_state_dict(state_dict_pfa1)
    model_pfa2.load_state_dict(state_dict_pfa2)
    model_pfa3.load_state_dict(state_dict_pfa3)
    model_pfa4.load_state_dict(state_dict_pfa4)
    
    # Get into evaluation (predictive posterior) mode
    # pidr1
    model_pidr1.eval()
    likelihood_pidr1.eval()
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_scaled).to(torch.float)
        observed_pred_test_pidr1 = likelihood_pidr1(model_pidr1(test_x))
    # pidr2
    model_pidr2.eval()
    likelihood_pidr2.eval()
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_scaled).to(torch.float)
        observed_pred_test_pidr2 = likelihood_pidr2(model_pidr2(test_x))
    # pidr3
    model_pidr3.eval()
    likelihood_pidr3.eval()
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_scaled).to(torch.float)
        observed_pred_test_pidr3 = likelihood_pidr3(model_pidr3(test_x))
    # pfa1
    model_pfa1.eval()
    likelihood_pfa1.eval()
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_scaled).to(torch.float)
        observed_pred_test_pfa1 = likelihood_pfa1(model_pfa1(test_x))
    # pfa2
    model_pfa2.eval()
    likelihood_pfa2.eval()
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_scaled).to(torch.float)
        observed_pred_test_pfa2 = likelihood_pfa2(model_pfa2(test_x))
    # pfa3
    model_pfa3.eval()
    likelihood_pfa3.eval()
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_scaled).to(torch.float)
        observed_pred_test_pfa3 = likelihood_pfa3(model_pfa3(test_x))
    # pfa4
    model_pfa4.eval()
    likelihood_pfa4.eval()
    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_scaled).to(torch.float)
        observed_pred_test_pfa4 = likelihood_pfa4(model_pfa4(test_x))
    # ridr
    param_pred = np.loadtxt(r'C:\Users\12734\OneDrive\重要文件\2_SensitivityAnalysis\Sensitivity-PythonCode\sensitivity-code\ResilienceAssessment\MainProcess\param_pred.txt')
    param_pred = np.hstack((params[:nn, :], np.exp(param_pred)))
    X_train_ridr_scaled = scaler.fit_transform(param_pred)
    X_predict_ridr = np.zeros((row, 12))
    X_predict_ridr[:, :9] = X_predict
    X_predict_ridr[:, 9] = observed_pred_test_pidr1.mean.numpy()
    X_predict_ridr[:, 10] = observed_pred_test_pidr2.mean.numpy()
    X_predict_ridr[:, 11] = observed_pred_test_pidr3.mean.numpy()
    X_test_ridr_scaled = scaler.transform(X_predict_ridr)
    train_x_ridr = torch.from_numpy(X_train_ridr_scaled).to(torch.float)
    train_y_ridr = torch.from_numpy(edpResults[:nn, 7]).to(torch.float)
    likelihood_ridr = gpytorch.likelihoods.GaussianLikelihood()
    model_ridr = ExactGPModel(train_x_ridr, train_y_ridr, likelihood_ridr, 12)
    model_ridr.load_state_dict(state_dict_ridr)

    model_ridr.eval()
    likelihood_ridr.eval()

    with torch.no_grad(), gpytorch.settings.fast_pred_var():
        test_x = torch.from_numpy(X_test_ridr_scaled).to(torch.float)
        observed_pred_test_ridr = likelihood_ridr(model_ridr(test_x))
    Y_predict = np.exp(np.hstack((observed_pred_test_pidr1.mean.numpy()[:, np.newaxis],
                                  observed_pred_test_pidr2.mean.numpy()[:, np.newaxis],
                                  observed_pred_test_pidr3.mean.numpy()[:, np.newaxis],
                                  observed_pred_test_pfa1.mean.numpy()[:, np.newaxis],
                                  observed_pred_test_pfa2.mean.numpy()[:, np.newaxis],
                                  observed_pred_test_pfa3.mean.numpy()[:, np.newaxis],
                                  observed_pred_test_pfa4.mean.numpy()[:, np.newaxis],
                                  observed_pred_test_ridr.mean.numpy()[:, np.newaxis])))
    
    return Y_predict