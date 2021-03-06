from sourceutils.misc.FileLocator import FileLocator
import re, os

class CodeTree:
    
    def __init__(self):
        self.codeTreeRoot = None
        
    def create(self, projectRoot, dirsNotToEnter):
        self.projectRoot = projectRoot
        self._normalizeProjectRoot()
        self._setProjectNameFromRoot()
        self._setCodeTreeRoot()
        
        self._createDirectoryStructure(dirsNotToEnter)
        
    def _createDirectoryStructure(self, dirsNotToEnter):
        
        f = FileLocator(self.projectRoot, '(.*)\.(c|cpp|cc|h|hpp|java)$')
        
        projectFiles = f.findFiles(dirsNotToEnter)
        for absoluteFilename in projectFiles:
            filename = self._getRelativeFilename(absoluteFilename)
            dirForSourceFile = self.codeTreeRoot + filename
            self._onFileDetection(filename, dirForSourceFile, absoluteFilename)
        
        print('Directory structure saved at ' + self.projectName)
    
    def _normalizeProjectRoot(self):
        # cut off last '/'
        if self.projectRoot[-1] == '/': self.projectRoot = self.projectRoot[:-1]
        
    def _setProjectNameFromRoot(self):
        self.projectName = '.' + self.projectRoot.split('/')[-1]

    def _setCodeTreeRoot(self):
        self.codeTreeRoot = self.projectName
    
    def _getRelativeFilename(self, filename):
        return re.sub('^' + self.projectRoot, '', filename)

    def _onFileDetection(self, filename, dirForSourceFile, absoluteFilename):
        # create dir for source file
        os.makedirs(dirForSourceFile)
        # copy original source-file to that dir
        os.system('cp %s %s/source' % (absoluteFilename, dirForSourceFile + '/'))
        
    def getCodeTreeRoot(self):
        return self.codeTreeRoot
    