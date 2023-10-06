#### Processing parameters (tailored for each sample)
nFeature_RNA_low=1000
percent.mt_top=10
nFeature_RNA_top=5000
dims.clustering=1:14
resolution.clustering = 0.4
dims.umap=1:14

SeuratProc <- function(sobj) {
  
  #### Filter data set based on RNA
  sobj <- subset(sobj, subset = nFeature_RNA > nFeature_RNA_low & 
                   percent.mt < percent.mt_top & 
                   nFeature_RNA < nFeature_RNA_top)
  sobj <- NormalizeData(sobj, normalization.method = "LogNormalize", 
                        scale.factor = 10000)
  sobj <- FindVariableFeatures(sobj, selection.method = "vst", 
                               nfeatures = 2000)
  
  #### Plot variable features (top 20 labelled)
  plot1 <- VariableFeaturePlot(sobj)
  print(LabelPoints(plot = plot1, points = head(VariableFeatures(sobj), 20), 
                    repel = TRUE)+theme_bw())
  
  ##### Scale data (RNA)
  sobj <- ScaleData(sobj, features = rownames(sobj))
  
  ##### Normalized and scale data (ADT)
  sobj <- NormalizeData(sobj, assay = "ADT", normalization.method = "CLR")
  sobj <- ScaleData(sobj, assay = "ADT")
  
  #### Assess cell cycle
  sobj <- CellCycleScoring(sobj, s.features = cc.genes$s.genes, 
                           g2m.features = cc.genes$g2m.genes, 
                           set.ident = TRUE)
  sobj <- ScaleData(sobj, vars.to.regress = c("S.Score", "G2M.Score", 
                                              "percent.mt"))
  
  #### Run PCA and print ElbowPlot
  sobj <- RunPCA(sobj, features = VariableFeatures(sobj), nfeatures.print=5)
  ElbowPlot(sobj)
  
  #### Run clustering based on transcriptome
  sobj <- FindNeighbors(sobj, dims = dims.clustering)
  sobj <- FindClusters(sobj, resolution = resolution.clustering)
  
  #### Run UMAP based on transcriptome
  sobj <- RunUMAP(sobj, dims = dims.umap)
  
  return(sobj)
  
}